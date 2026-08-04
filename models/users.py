"""
User model
"""

from sqlalchemy import Column, Integer, BigInteger, String, DateTime, Boolean, Index
from sqlalchemy.sql import func
from models.base import BaseModel

class User(BaseModel):
    __tablename__ = "users"
    
    telegram_id = Column(BigInteger, unique=True, nullable=False, index=True)
    username = Column(String(100), nullable=True)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    
    plan = Column(String(20), default="free")
    is_premium = Column(Boolean, default=False)
    premium_expires_at = Column(DateTime, nullable=True)
    
    coins = Column(Integer, default=0)
    total_coins_earned = Column(Integer, default=0)
    total_coins_spent = Column(Integer, default=0)
    
    referral_code = Column(String(20), unique=True, nullable=False)
    referred_by = Column(BigInteger, nullable=True, index=True)
    total_referrals = Column(Integer, default=0)
    
    total_searches = Column(Integer, default=0)
    total_found = Column(Integer, default=0)
    last_search_at = Column(DateTime, nullable=True)
    
    daily_searches = Column(Integer, default=0)
    daily_reset_at = Column(DateTime, nullable=True)
    
    is_active = Column(Boolean, default=True)
    is_banned = Column(Boolean, default=False)
