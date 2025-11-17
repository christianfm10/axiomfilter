"""
Filter logic for Axiom Trade WebSocket messages
Contains functions to validate and filter messages based on configured criteria
"""

from typing import List, Dict, Any
from models import UpdatePulseItem, XHRPulseResponse
from config import FilterConfig


class MessageFilter:
    """Handles filtering logic for different message types"""

    def __init__(self, config: FilterConfig):
        """
        Initialize the filter with a configuration

        Args:
            config: FilterConfig instance with filter settings
        """
        self.config = config

    def should_keep_update_pulse_item(self, item_array: List[Any]) -> bool:
        """
        Determine if an update_pulse item should be kept based on filters

        Args:
            item_array: Array representing an update_pulse item

        Returns:
            True if the item passes filters, False otherwise
        """
        # Parse the item
        item = UpdatePulseItem.from_array(item_array)

        # Filter by dev address if enabled
        if self.config.FILTER_BY_DEV_ADDRESS:
            if item.dev_address in self.config.DEV_ADDRESSES:
                return True

        # Filter by funding wallet if enabled
        if self.config.FILTER_BY_FUNDING_WALLET:
            if item.dev_wallet_funding:
                if (
                    item.dev_wallet_funding.funding_wallet_address
                    in self.config.FUNDER_ADDRESSES
                ):
                    return True

        # If no filters matched, exclude the item
        return False

    def filter_update_pulse_content(self, content: List[List[Any]]) -> List[List[Any]]:
        """
        Filter the content array of an update_pulse message

        Args:
            content: List of update_pulse items (each item is an array)

        Returns:
            Filtered list containing only items that pass the filters
        """
        return [item for item in content if self.should_keep_update_pulse_item(item)]

    def should_keep_xhr_response(self, response_dict: Dict[str, Any]) -> bool:
        """
        Determine if an XHR /pulse response should be kept based on filters

        Args:
            response_dict: Dictionary representing a pulse response

        Returns:
            True if the response passes filters, False otherwise
        """
        # Parse the response
        response = XHRPulseResponse.from_dict(response_dict)

        # Filter by dev address if enabled
        if self.config.FILTER_BY_DEV_ADDRESS:
            if response.dev_address in self.config.DEV_ADDRESSES:
                return True

        # Filter by funding wallet if enabled
        if self.config.FILTER_BY_FUNDING_WALLET:
            if response.dev_wallet_funding:
                if (
                    response.dev_wallet_funding.funding_wallet_address
                    in self.config.FUNDER_ADDRESSES
                ):
                    return True

        # If no filters matched, exclude the response
        return False

    def filter_xhr_responses(
        self, responses: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Filter a list of XHR /pulse responses

        Args:
            responses: List of pulse response dictionaries

        Returns:
            Filtered list containing only responses that pass the filters
        """
        return [resp for resp in responses if self.should_keep_xhr_response(resp)]

    def should_keep_new_pair(self, content: Dict[str, Any]) -> bool:
        """
        Determine if a new_pairs message should be kept based on filters
        Currently returns True for all new pairs (can be customized)

        Args:
            content: Dictionary representing new pair content

        Returns:
            True if the pair should be kept, False otherwise
        """
        # You can add custom filters for new pairs here
        # For example, filter by deployer address, protocol, etc.

        # Example: Filter by deployer address
        # deployer = content.get("deployer_address", "")
        # if deployer in self.config.DEV_ADDRESSES:
        #     return True

        # By default, keep all new pairs
        return True


class FilterStats:
    """Track statistics about filtered messages"""

    def __init__(self):
        self.total_update_pulse_items = 0
        self.filtered_update_pulse_items = 0
        self.total_xhr_responses = 0
        self.filtered_xhr_responses = 0
        self.total_new_pairs = 0
        self.filtered_new_pairs = 0

    def record_update_pulse(self, total: int, filtered: int) -> None:
        """Record statistics for an update_pulse message"""
        self.total_update_pulse_items += total
        self.filtered_update_pulse_items += filtered

    def record_xhr(self, total: int, filtered: int) -> None:
        """Record statistics for XHR responses"""
        self.total_xhr_responses += total
        self.filtered_xhr_responses += filtered

    def record_new_pair(self, kept: bool) -> None:
        """Record statistics for a new_pairs message"""
        self.total_new_pairs += 1
        if kept:
            self.filtered_new_pairs += 1

    def get_summary(self) -> str:
        """Get a summary of filter statistics"""
        lines = [
            "=== Filter Statistics ===",
            f"Update Pulse: {self.filtered_update_pulse_items}/{self.total_update_pulse_items} items kept",
            f"XHR Responses: {self.filtered_xhr_responses}/{self.total_xhr_responses} items kept",
            f"New Pairs: {self.filtered_new_pairs}/{self.total_new_pairs} messages kept",
        ]
        return "\n".join(lines)

    def reset(self) -> None:
        """Reset all statistics"""
        self.total_update_pulse_items = 0
        self.filtered_update_pulse_items = 0
        self.total_xhr_responses = 0
        self.filtered_xhr_responses = 0
        self.total_new_pairs = 0
        self.filtered_new_pairs = 0
