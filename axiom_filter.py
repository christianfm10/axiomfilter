"""
Axiom Trade WebSocket Filter - mitmproxy addon
Filters WebSocket messages and XHR responses from axiom.trade based on configured criteria
"""

from mitmproxy import ctx
from mitmproxy.http import HTTPFlow
from mitmproxy.websocket import WebSocketMessage
import json
import base64
from typing import Optional

from config import config, FilterConfig
from filters import MessageFilter, FilterStats


class AxiomTradeFilter:
    """
    mitmproxy addon to filter Axiom Trade WebSocket messages and HTTP responses

    Filters:
    - WebSocket messages from update_pulse_v2 room
    - XHR responses from /pulse endpoint
    - Optionally filters new_pairs room messages
    """

    def __init__(self, custom_config: Optional[FilterConfig] = None):
        """
        Initialize the filter addon

        Args:
            custom_config: Optional custom configuration (uses default if None)
        """
        self.config = custom_config or config
        self.filter = MessageFilter(self.config)
        self.stats = FilterStats()

        if self.config.ENABLE_LOGGING:
            ctx.log.info("=" * 60)
            ctx.log.info("Axiom Trade Filter Initialized")
            ctx.log.info(f"Target Host: {self.config.TARGET_HOST}")
            ctx.log.info(f"Filter by Dev Address: {self.config.FILTER_BY_DEV_ADDRESS}")
            ctx.log.info(
                f"Filter by Funding Wallet: {self.config.FILTER_BY_FUNDING_WALLET}"
            )
            ctx.log.info(f"Dev Addresses: {len(self.config.DEV_ADDRESSES)}")
            ctx.log.info(f"Funder Addresses: {len(self.config.FUNDER_ADDRESSES)}")
            ctx.log.info("=" * 60)

    def _is_target_host(self, flow: HTTPFlow) -> bool:
        """
        Check if the flow is from the target host

        Args:
            flow: HTTP flow to check

        Returns:
            True if flow is from target host, False otherwise
        """
        try:
            host = flow.server_conn.address[0] if flow.server_conn else ""
        except Exception:
            host = ""

        pretty_host = flow.request.pretty_host

        return self.config.TARGET_HOST in host or self.config.TARGET_HOST in pretty_host

    def _decode_message_content(self, content: bytes) -> str:
        """
        Decode WebSocket message content to string

        Args:
            content: Raw message content

        Returns:
            Decoded string or base64 encoded representation
        """
        if isinstance(content, bytes):
            try:
                return content.decode("utf-8")
            except Exception:
                # If not decodable as UTF-8, return base64
                return "base64:" + base64.b64encode(content).decode()
        return str(content)

    def _get_room_name(self, text: str) -> Optional[str]:
        """
        Extract room name from message text

        Args:
            text: Message text

        Returns:
            Room name if found, None otherwise
        """
        # Check first 50 characters for room name
        text_start = text.lower()[:50]

        if self.config.ROOM_NEW_PAIRS in text_start:
            return self.config.ROOM_NEW_PAIRS
        elif self.config.ROOM_UPDATE_PULSE in text_start:
            return self.config.ROOM_UPDATE_PULSE

        return None

    def _filter_update_pulse_message(
        self, message: WebSocketMessage, text: str
    ) -> None:
        """
        Filter an update_pulse_v2 WebSocket message

        Args:
            message: WebSocket message to filter
            text: Decoded message text
        """
        try:
            data = json.loads(text)

            if "content" not in data or not isinstance(data["content"], list):
                return

            original_count = len(data["content"])

            # Apply filters
            filtered_content = self.filter.filter_update_pulse_content(data["content"])

            # Update statistics
            self.stats.record_update_pulse(original_count, len(filtered_content))

            if self.config.ENABLE_LOGGING:
                ctx.log.info(
                    f"Update Pulse: {len(filtered_content)}/{original_count} items kept"
                )

            # If no items pass the filter, drop the message
            if len(filtered_content) == 0:
                message.drop()
                if self.config.VERBOSE_LOGGING:
                    ctx.log.info("Message dropped - no items passed filter")
                return

            # Update message content with filtered data
            data["content"] = filtered_content
            new_text = json.dumps(data)

            if message.is_text:
                message.text = new_text

        except json.JSONDecodeError as e:
            if self.config.ENABLE_LOGGING:
                ctx.log.error(f"Failed to decode update_pulse message: {e}")
        except Exception as e:
            if self.config.ENABLE_LOGGING:
                ctx.log.error(f"Error filtering update_pulse message: {e}")

    def _filter_new_pairs_message(self, message: WebSocketMessage, text: str) -> None:
        """
        Filter a new_pairs WebSocket message

        Args:
            message: WebSocket message to filter
            text: Decoded message text
        """
        try:
            data = json.loads(text)

            if "content" not in data:
                return

            # Check if message should be kept
            should_keep = self.filter.should_keep_new_pair(data["content"])

            # Update statistics
            self.stats.record_new_pair(should_keep)

            if not should_keep:
                message.drop()
                if self.config.VERBOSE_LOGGING:
                    ctx.log.info("New pair message dropped")
            elif self.config.VERBOSE_LOGGING:
                token_name = data["content"].get("token_name", "Unknown")
                ctx.log.info(f"New pair kept: {token_name}")

        except json.JSONDecodeError as e:
            if self.config.ENABLE_LOGGING:
                ctx.log.error(f"Failed to decode new_pairs message: {e}")
        except Exception as e:
            if self.config.ENABLE_LOGGING:
                ctx.log.error(f"Error filtering new_pairs message: {e}")

    def websocket_message(self, flow: HTTPFlow) -> None:
        """
        Hook called for each WebSocket message

        Args:
            flow: HTTP flow containing WebSocket messages
        """
        # Check if this is from target host
        if not self._is_target_host(flow):
            return

        # Get the last message
        if not flow.websocket or not flow.websocket.messages:
            return

        message = flow.websocket.messages[-1]

        # Only process messages from server to client
        if message.from_client:
            return

        # Decode message content
        text = self._decode_message_content(message.content)

        # Determine room and apply appropriate filter
        room = self._get_room_name(text)

        if room == self.config.ROOM_UPDATE_PULSE:
            self._filter_update_pulse_message(message, text)
        elif room == self.config.ROOM_NEW_PAIRS:
            self._filter_new_pairs_message(message, text)
            message.drop()

    def response(self, flow: HTTPFlow) -> None:
        """
        Hook called for each HTTP response

        Args:
            flow: HTTP flow
        """
        # Check if this is a /pulse POST request
        if flow.request.path != "/pulse" or flow.request.method != "POST":
            return

        # Check if this is from target host
        if not self._is_target_host(flow):
            return

        try:
            # Parse response content
            content = json.loads(flow.response.content)

            # Handle both single object and array responses
            if isinstance(content, list):
                original_count = len(content)

                # Apply filters
                filtered_content = self.filter.filter_xhr_responses(content)

                # Update statistics
                self.stats.record_xhr(original_count, len(filtered_content))

                if self.config.ENABLE_LOGGING:
                    ctx.log.info(
                        f"XHR /pulse: {len(filtered_content)}/{original_count} items kept"
                    )

                # Update response
                flow.response.content = json.dumps(filtered_content).encode("utf-8")
            elif isinstance(content, dict):
                # Single response - check if it should be kept
                should_keep = self.filter.should_keep_xhr_response(content)

                self.stats.record_xhr(1, 1 if should_keep else 0)

                if not should_keep:
                    # Return empty response
                    flow.response.content = json.dumps({}).encode("utf-8")
                    if self.config.VERBOSE_LOGGING:
                        ctx.log.info("XHR response filtered out")

        except json.JSONDecodeError as e:
            if self.config.ENABLE_LOGGING:
                ctx.log.error(f"Failed to decode /pulse response: {e}")
        except Exception as e:
            if self.config.ENABLE_LOGGING:
                ctx.log.error(f"Error filtering /pulse response: {e}")

    def done(self) -> None:
        """
        Hook called when mitmproxy is shutting down
        """
        if self.config.ENABLE_LOGGING:
            ctx.log.info("=" * 60)
            ctx.log.info(self.stats.get_summary())
            ctx.log.info("=" * 60)


# Create addon instance for mitmproxy
addons = [AxiomTradeFilter()]
