"""
Configuration file for Axiom Trade WebSocket Filter
Contains all filter settings, wallet addresses, and room configurations
"""

from typing import Set
from dataclasses import dataclass


@dataclass
class FilterConfig:
    """Main configuration for the filter"""

    # Target host to filter
    TARGET_HOST: str = "axiom.trade"

    # WebSocket room names
    ROOM_NEW_PAIRS: str = "new_pairs"
    ROOM_UPDATE_PULSE: str = "update_pulse_v2"

    # Known wallet addresses
    BINANCE_ADDRESS: str = "5tzFkiKscXHK5ZXCGbXZxdw7gTjjD1mBwuoFbhUvuAi9"
    KUCOIN_ADDRESS: str = "BmFdpraQhkiDQE6SnfG5omcA1VwzqfXrwtNYBwWTymy6"
    BYBIT_ADDRESS: str = "iGdFcQoyR2MwbXMHQskhmNsqddZ6rinsipHc4TNSdwu"
    MEXC_ADDRESS: str = "ASTyfSima4LLAdDgoFGkgqoKowG1LZFDr9fAQrg7iaJZ"

    # Developer addresses to filter
    DEV_ADDRESSES: Set[str] | None = None

    # Funding wallet addresses to filter
    FUNDER_ADDRESSES: Set[str] | None = None

    # Enable/disable specific filters
    FILTER_BY_DEV_ADDRESS: bool = False
    FILTER_BY_FUNDING_WALLET: bool = True

    # Logging
    ENABLE_LOGGING: bool = False
    VERBOSE_LOGGING: bool = False

    def __post_init__(self):
        """Initialize sets after dataclass creation"""
        if self.DEV_ADDRESSES is None:
            self.DEV_ADDRESSES = {
                # "54bV9JqbBYH5hVCXe41mkdSioPPBZULCrJYfHVfagnME",
                # "6muPgMoshvTJQzJ3EteaGLxpz5ZTDYHZ5HzMQCNiZ4hh",
                "asdsadasdsa",
            }

        if self.FUNDER_ADDRESSES is None:
            self.FUNDER_ADDRESSES = {
                self.KUCOIN_ADDRESS,
                self.MEXC_ADDRESS,
                self.BYBIT_ADDRESS,
            }

    def add_dev_address(self, address: str) -> None:
        """Add a developer address to the filter list"""
        self.DEV_ADDRESSES.add(address)

    def add_funder_address(self, address: str) -> None:
        """Add a funder address to the filter list"""
        self.FUNDER_ADDRESSES.add(address)

    def remove_dev_address(self, address: str) -> None:
        """Remove a developer address from the filter list"""
        self.DEV_ADDRESSES.discard(address)

    def remove_funder_address(self, address: str) -> None:
        """Remove a funder address from the filter list"""
        self.FUNDER_ADDRESSES.discard(address)


# Create a default configuration instance
config = FilterConfig()
