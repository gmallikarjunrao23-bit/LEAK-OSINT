"""
Configuration — All env variables from Railway
"""

import os
from typing import List, Optional

class Settings:
    """Bot settings from environment — Railway variables"""
    
    # Bot Token
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    
    # Database — Default SQLite if not provided
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///leakbot.db")
    
    # Redis (optional)
    REDIS_URL: Optional[str] = os.getenv("REDIS_URL", None)
    
    # Leak API
    LEAK_API_KEY: str = os.getenv("LEAK_API_KEY", "SAHILS")
    LEAK_API_URL: str = os.getenv("LEAK_API_URL", "https://sahilxalone.xyz/api/leakpro")
    
    # Admins — comma separated IDs
    ADMIN_IDS: List[int] = [
        int(x.strip()) for x in os.getenv("ADMIN_IDS", "").split(",") 
        if x.strip() and x.strip().isdigit()
    ]
    
    # UPI Payment — YOUR UPI ID
    UPI_ID: str = os.getenv("UPI_ID", "9866583926@ax1")
    
    # Pricing
    PREMIUM_PRICE: int = int(os.getenv("PREMIUM_PRICE", "100"))
    ENTERPRISE_PRICE: int = int(os.getenv("ENTERPRISE_PRICE", "500"))
    PREMIUM_DAYS: int = int(os.getenv("PREMIUM_DAYS", "30"))
    ENTERPRISE_DAYS: int = int(os.getenv("ENTERPRISE_DAYS", "365"))
    
    # Coin System
    FREE_COINS_ON_SIGNUP: int = int(os.getenv("FREE_COINS_ON_SIGNUP", "10"))
    COINS_PER_SEARCH: int = int(os.getenv("COINS_PER_SEARCH", "1"))
    REFERRAL_REWARD_COINS: int = int(os.getenv("REFERRAL_REWARD_COINS", "5"))
    
    # Daily Limits
    FREE_DAILY_SEARCHES: int = int(os.getenv("FREE_DAILY_SEARCHES", "5"))
    PREMIUM_DAILY_SEARCHES: int = int(os.getenv("PREMIUM_DAILY_SEARCHES", "100"))
    ENTERPRISE_DAILY_SEARCHES: int = int(os.getenv("ENTERPRISE_DAILY_SEARCHES", "9999"))

settings = Settings()
