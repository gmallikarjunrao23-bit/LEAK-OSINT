"""
Payment model — UPI payments
"""

from sqlalchemy import Column, Integer, BigInteger, String, DateTime, JSON, Float, Boolean, Text, Index
from sqlalchemy.sql import func
from models.base import BaseModel

class Payment(BaseModel):
    __tablename__ = "payments"
    
    user_id = Column(BigInteger, nullable=False, index=True)
    username = Column(String(100), nullable=True)
    transaction_id = Column(String(100), unique=True, nullable=True)
    screenshot_url = Column(String(500), nullable=True)
    
    amount = Column(Float, nullable=False)
    plan = Column(String(20), nullable=False)
    
    status = Column(String(20), default="pending")
    admin_notes = Column(Text, nullable=True)
    admin_id = Column(BigInteger, nullable=True)
    
    upi_id = Column(String(100), nullable=True)
    upi_txn_ref = Column(String(100), nullable=True)
    
    submitted_at = Column(DateTime, server_default=func.now())
    reviewed_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
