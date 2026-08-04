"""
Query model
"""

from sqlalchemy import Column, Integer, BigInteger, String, DateTime, JSON, Index
from models.base import BaseModel

class Query(BaseModel):
    __tablename__ = "queries"
    
    user_id = Column(BigInteger, nullable=False, index=True)
    target = Column(String(200), nullable=False)
    target_type = Column(String(20))
    result = Column(JSON, nullable=True)
    found_count = Column(Integer, default=0)
    coins_used = Column(Integer, default=1)
    response_time_ms = Column(Integer, nullable=True)
    api_status = Column(Integer, nullable=True)
    error_message = Column(String(500), nullable=True)
