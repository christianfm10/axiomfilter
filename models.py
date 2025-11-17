"""
Data models for Axiom Trade WebSocket messages
Defines the structure of different message types and responses
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any, List


@dataclass
class DevWalletFunding:
    """Developer wallet funding information"""

    wallet_address: str
    funding_wallet_address: str
    signature: str
    amount_sol: float
    funded_at: str

    @classmethod
    def from_ws_array(
        cls, data: Optional[Dict[str, Any]]
    ) -> Optional["DevWalletFunding"]:
        """Create from WebSocket array format (index 39)"""
        if not data:
            return None

        return cls(
            wallet_address=data.get("walletAddress", ""),
            funding_wallet_address=data.get("fundingWalletAddress", ""),
            signature=data.get("signature", ""),
            amount_sol=data.get("amountSol", 0.0),
            funded_at=data.get("fundedAt", ""),
        )

    @classmethod
    def from_xhr(cls, data: Optional[Dict[str, Any]]) -> Optional["DevWalletFunding"]:
        """Create from XHR response format"""
        if not data:
            return None

        return cls(
            wallet_address=data.get("walletAddress", ""),
            funding_wallet_address=data.get("fundingWalletAddress", ""),
            signature=data.get("signature", ""),
            amount_sol=data.get("amountSol", 0.0),
            funded_at=data.get("fundedAt", ""),
        )


@dataclass
class ProtocolDetails:
    """Protocol details for a token pair"""

    creator: str
    is_token_side_x: Optional[bool] = None
    token_program: Optional[str] = None
    pair_sol_account: Optional[str] = None
    pair_token_account: Optional[str] = None

    # Pump V1 specific fields
    global_addr: Optional[str] = None
    fee_recipient: Optional[str] = None
    associated_bonding_curve: Optional[str] = None
    event_authority: Optional[str] = None
    is_offchain: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ProtocolDetails":
        """Create from dictionary"""
        return cls(
            creator=data.get("creator", ""),
            is_token_side_x=data.get("isTokenSideX"),
            token_program=data.get("tokenProgram"),
            pair_sol_account=data.get("pairSolAccount"),
            pair_token_account=data.get("pairTokenAccount"),
            global_addr=data.get("global"),
            fee_recipient=data.get("feeRecipient"),
            associated_bonding_curve=data.get("associatedBondingCurve"),
            event_authority=data.get("eventAuthority"),
            is_offchain=data.get("isOffchain"),
        )


@dataclass
class UpdatePulseItem:
    """
    Represents an item from the update_pulse_v2 WebSocket message
    Data is received as an array with fixed indices
    """

    pair_address: str  # Index 0
    token_address: str  # Index 1
    dev_address: str  # Index 2
    token_name: str  # Index 3
    token_ticker: str  # Index 4
    token_image: Optional[str]  # Index 5
    token_decimals: int  # Index 6
    protocol: str  # Index 7
    protocol_details: Optional[ProtocolDetails]  # Index 8
    website: Optional[str]  # Index 9
    twitter: Optional[str]  # Index 10
    telegram: Optional[str]  # Index 11
    discord: Optional[str]  # Index 12
    top_10_holders_percent: float  # Index 13
    dev_holds_percent: float  # Index 14
    snipers_hold_percent: float  # Index 15
    insiders_hold_percent: float  # Index 16
    bundlers_hold_percent: float  # Index 17
    volume_sol: float  # Index 18
    market_cap_sol: float  # Index 19
    fees_sol: float  # Index 20
    liquidity_sol: float  # Index 21
    liquidity_token: float  # Index 22
    num_txns: int  # Index 23
    num_buys: int  # Index 24
    num_sells: int  # Index 25
    bonding_curve_percent: float  # Index 26
    supply: float  # Index 27
    num_holders: int  # Index 28
    num_trading_bot_users: int  # Index 29
    migrated_date: Optional[str]  # Index 30
    extra: Optional[Dict[str, Any]]  # Index 31
    field_32: Any  # Index 32 (unknown)
    migrated_tokens: Optional[int]  # Index 33
    first_mint_date: Optional[str]  # Index 34
    field_35: Any  # Index 35 (unknown)
    twitter_handle_history: List  # Index 36
    field_37: Any  # Index 37 (unknown)
    dex_paid: bool  # Index 38
    dev_wallet_funding: Optional[DevWalletFunding]  # Index 39
    kol_count: int  # Index 40
    dev_tokens: Optional[int]  # Index 41
    field_42: Any  # Index 42 (unknown)

    @classmethod
    def from_array(cls, data: List[Any]) -> "UpdatePulseItem":
        """Create from WebSocket array format"""
        protocol_details = None
        if len(data) > 8 and isinstance(data[8], dict):
            protocol_details = ProtocolDetails.from_dict(data[8])

        dev_wallet_funding = None
        if len(data) > 39 and data[39]:
            dev_wallet_funding = DevWalletFunding.from_ws_array(data[39])

        return cls(
            pair_address=data[0] if len(data) > 0 else "",
            token_address=data[1] if len(data) > 1 else "",
            dev_address=data[2] if len(data) > 2 else "",
            token_name=data[3] if len(data) > 3 else "",
            token_ticker=data[4] if len(data) > 4 else "",
            token_image=data[5] if len(data) > 5 else None,
            token_decimals=data[6] if len(data) > 6 else 0,
            protocol=data[7] if len(data) > 7 else "",
            protocol_details=protocol_details,
            website=data[9] if len(data) > 9 else None,
            twitter=data[10] if len(data) > 10 else None,
            telegram=data[11] if len(data) > 11 else None,
            discord=data[12] if len(data) > 12 else None,
            top_10_holders_percent=data[13] if len(data) > 13 else 0.0,
            dev_holds_percent=data[14] if len(data) > 14 else 0.0,
            snipers_hold_percent=data[15] if len(data) > 15 else 0.0,
            insiders_hold_percent=data[16] if len(data) > 16 else 0.0,
            bundlers_hold_percent=data[17] if len(data) > 17 else 0.0,
            volume_sol=data[18] if len(data) > 18 else 0.0,
            market_cap_sol=data[19] if len(data) > 19 else 0.0,
            fees_sol=data[20] if len(data) > 20 else 0.0,
            liquidity_sol=data[21] if len(data) > 21 else 0.0,
            liquidity_token=data[22] if len(data) > 22 else 0.0,
            num_txns=data[23] if len(data) > 23 else 0,
            num_buys=data[24] if len(data) > 24 else 0,
            num_sells=data[25] if len(data) > 25 else 0,
            bonding_curve_percent=data[26] if len(data) > 26 else 0.0,
            supply=data[27] if len(data) > 27 else 0.0,
            num_holders=data[28] if len(data) > 28 else 0,
            num_trading_bot_users=data[29] if len(data) > 29 else 0,
            migrated_date=data[30] if len(data) > 30 else None,
            extra=data[31] if len(data) > 31 else None,
            field_32=data[32] if len(data) > 32 else None,
            migrated_tokens=data[33] if len(data) > 33 else None,
            first_mint_date=data[34] if len(data) > 34 else None,
            field_35=data[35] if len(data) > 35 else None,
            twitter_handle_history=data[36] if len(data) > 36 else [],
            field_37=data[37] if len(data) > 37 else None,
            dex_paid=data[38] if len(data) > 38 else False,
            dev_wallet_funding=dev_wallet_funding,
            kol_count=data[40] if len(data) > 40 else 0,
            dev_tokens=data[41] if len(data) > 41 else None,
            field_42=data[42] if len(data) > 42 else None,
        )


@dataclass
class NewPairContent:
    """Content of a new_pairs WebSocket message"""

    pair_address: str
    signature: str
    token_address: str
    token_name: str
    token_ticker: str
    token_image: Optional[str]
    token_uri: str
    token_decimals: int
    pair_sol_account: str
    pair_token_account: str
    protocol: str
    protocol_details: Dict[str, Any]
    created_at: str
    website: Optional[str]
    twitter: Optional[str]
    telegram: Optional[str]
    discord: Optional[str]
    mint_authority: Optional[str]
    open_trading: str
    deployer_address: str
    supply: float
    initial_liquidity_sol: float
    initial_liquidity_token: float
    top_10_holders: float
    lp_burned: float
    updated_at: str
    dev_holds_percent: float
    snipers_hold_percent: float
    freeze_authority: Optional[str]
    extra: Optional[Any]
    slot: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "NewPairContent":
        """Create from dictionary"""
        return cls(
            pair_address=data.get("pair_address", ""),
            signature=data.get("signature", ""),
            token_address=data.get("token_address", ""),
            token_name=data.get("token_name", ""),
            token_ticker=data.get("token_ticker", ""),
            token_image=data.get("token_image"),
            token_uri=data.get("token_uri", ""),
            token_decimals=data.get("token_decimals", 0),
            pair_sol_account=data.get("pair_sol_account", ""),
            pair_token_account=data.get("pair_token_account", ""),
            protocol=data.get("protocol", ""),
            protocol_details=data.get("protocol_details", {}),
            created_at=data.get("created_at", ""),
            website=data.get("website"),
            twitter=data.get("twitter"),
            telegram=data.get("telegram"),
            discord=data.get("discord"),
            mint_authority=data.get("mint_authority"),
            open_trading=data.get("open_trading", ""),
            deployer_address=data.get("deployer_address", ""),
            supply=data.get("supply", 0.0),
            initial_liquidity_sol=data.get("initial_liquidity_sol", 0.0),
            initial_liquidity_token=data.get("initial_liquidity_token", 0.0),
            top_10_holders=data.get("top_10_holders", 0.0),
            lp_burned=data.get("lp_burned", 0.0),
            updated_at=data.get("updated_at", ""),
            dev_holds_percent=data.get("dev_holds_percent", 0.0),
            snipers_hold_percent=data.get("snipers_hold_percent", 0.0),
            freeze_authority=data.get("freeze_authority"),
            extra=data.get("extra"),
            slot=data.get("slot", 0),
        )


@dataclass
class XHRPulseResponse:
    """Response from /pulse XHR endpoint"""

    pair_address: str
    token_address: str
    dev_address: str
    token_name: str
    token_ticker: str
    token_image: Optional[str]
    token_decimals: int
    protocol: str
    protocol_details: Dict[str, Any]
    website: Optional[str]
    twitter: Optional[str]
    telegram: Optional[str]
    discord: Optional[str]
    top_10_holders_percent: float
    dev_holds_percent: float
    dev_pair_count: int
    snipers_hold_percent: float
    insiders_hold_percent: float
    bundlers_hold_percent: float
    volume_sol: float
    market_cap_sol: float
    fees_sol: float
    liquidity_sol: float
    liquidity_token: float
    bonding_curve_percent: float
    supply: float
    num_txns: int
    num_buys: int
    num_sells: int
    num_holders: int
    num_trading_bot_users: int
    created_at: str
    extra: Optional[Dict[str, Any]]
    dex_paid: bool
    migration_count: int
    twitter_handle_history: List
    open_trading: str
    dev_wallet_funding: Optional[DevWalletFunding]
    kol_count: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "XHRPulseResponse":
        """Create from dictionary"""
        dev_wallet_funding = None
        if "devWalletFunding" in data and data["devWalletFunding"]:
            dev_wallet_funding = DevWalletFunding.from_xhr(data["devWalletFunding"])

        return cls(
            pair_address=data.get("pairAddress", ""),
            token_address=data.get("tokenAddress", ""),
            dev_address=data.get("devAddress", ""),
            token_name=data.get("tokenName", ""),
            token_ticker=data.get("tokenTicker", ""),
            token_image=data.get("tokenImage"),
            token_decimals=data.get("tokenDecimals", 0),
            protocol=data.get("protocol", ""),
            protocol_details=data.get("protocolDetails", {}),
            website=data.get("website"),
            twitter=data.get("twitter"),
            telegram=data.get("telegram"),
            discord=data.get("discord"),
            top_10_holders_percent=data.get("top10HoldersPercent", 0.0),
            dev_holds_percent=data.get("devHoldsPercent", 0.0),
            dev_pair_count=data.get("devPairCount", 0),
            snipers_hold_percent=data.get("snipersHoldPercent", 0.0),
            insiders_hold_percent=data.get("insidersHoldPercent", 0.0),
            bundlers_hold_percent=data.get("bundlersHoldPercent", 0.0),
            volume_sol=data.get("volumeSol", 0.0),
            market_cap_sol=data.get("marketCapSol", 0.0),
            fees_sol=data.get("feesSol", 0.0),
            liquidity_sol=data.get("liquiditySol", 0.0),
            liquidity_token=data.get("liquidityToken", 0.0),
            bonding_curve_percent=data.get("bondingCurvePercent", 0.0),
            supply=data.get("supply", 0.0),
            num_txns=data.get("numTxns", 0),
            num_buys=data.get("numBuys", 0),
            num_sells=data.get("numSells", 0),
            num_holders=data.get("numHolders", 0),
            num_trading_bot_users=data.get("numTradingBotUsers", 0),
            created_at=data.get("createdAt", ""),
            extra=data.get("extra"),
            dex_paid=data.get("dexPaid", False),
            migration_count=data.get("migrationCount", 0),
            twitter_handle_history=data.get("twitterHandleHistory", []),
            open_trading=data.get("openTrading", ""),
            dev_wallet_funding=dev_wallet_funding,
            kol_count=data.get("kolCount", 0),
        )
