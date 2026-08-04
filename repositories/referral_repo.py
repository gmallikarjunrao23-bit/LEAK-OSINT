"""
Referral repository
"""

from typing import Optional
from models import Referral
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.base import BaseRepository
from models.referral import Referral

class ReferralRepository(BaseRepository[Referral]):
    def __init__(self, session: AsyncSession):
        super().__init__(Referral, session)
    
    async def get_by_referred(self, referred_id: int) -> Optional[Referral]:
        return await self.get(referred_id=referred_id)
    
    async def create_referral(self, referrer_id: int, referred_id: int, coins_awarded: int) -> Referral:
        return await self.create(
            referrer_id=referrer_id,
            referred_id=referred_id,
            coins_awarded=coins_awarded
        )
