"""
Referral model
"""

from sqlalchemy import Column, Integer, BigInteger, String, DateTime, Boolean
from models.base import BaseModel

class Referral(BaseModel):
    __tablename__ = "referrals"
    
    referrer_id = Column(BigInteger, nullable=False, index=True)
    referred_id = Column(BigInteger, unique=True, nullable=False, index=True)
    coins_awarded = Column(Integer, default=0)
    is_claimed = Column(Boolean, default=False)
    claimed_at = Column(DateTime, nullable=True)
