"""
User repository
"""

from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
import random
import string
from repositories.base import BaseRepository
from models import User
from repositories.base import BaseRepository

class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)
    
    def _generate_referral_code(self) -> str:
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    
    async def get_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        return await self.get(telegram_id=telegram_id)
    
    async def get_by_referral_code(self, referral_code: str) -> Optional[User]:
        return await self.get(referral_code=referral_code)
    
    async def create_user(self, telegram_id: int, first_name: str, username: str = None,
                          last_name: str = None) -> User:
        return await self.create(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            referral_code=self._generate_referral_code(),
            coins=10
        )
    
    async def add_coins(self, telegram_id: int, amount: int) -> Optional[User]:
        user = await self.get_by_telegram_id(telegram_id)
        if user:
            user.coins += amount
            user.total_coins_earned += amount
            await self.session.commit()
            await self.session.refresh(user)
        return user
    
    async def deduct_coins(self, telegram_id: int, amount: int) -> Optional[User]:
        user = await self.get_by_telegram_id(telegram_id)
        if user and user.coins >= amount:
            user.coins -= amount
            user.total_coins_spent += amount
            await self.session.commit()
            await self.session.refresh(user)
            return user
        return None
    
    async def set_premium(self, telegram_id: int, days: int) -> Optional[User]:
        user = await self.get_by_telegram_id(telegram_id)
        if user:
            user.is_premium = True
            user.plan = "premium"
            user.premium_expires_at = datetime.utcnow() + timedelta(days=days)
            await self.session.commit()
            await self.session.refresh(user)
        return user
    
    async def set_enterprise(self, telegram_id: int, days: int) -> Optional[User]:
        user = await self.get_by_telegram_id(telegram_id)
        if user:
            user.is_premium = True
            user.plan = "enterprise"
            user.premium_expires_at = datetime.utcnow() + timedelta(days=days)
            await self.session.commit()
            await self.session.refresh(user)
        return user
    
    async def check_premium_status(self, telegram_id: int) -> bool:
        user = await self.get_by_telegram_id(telegram_id)
        if not user or not user.is_premium:
            return False
        if user.premium_expires_at and user.premium_expires_at < datetime.utcnow():
            user.is_premium = False
            user.plan = "free"
            await self.session.commit()
            return False
        return True
    
    async def increment_searches(self, telegram_id: int) -> Optional[User]:
        user = await self.get_by_telegram_id(telegram_id)
        if user:
            user.total_searches += 1
            user.last_search_at = datetime.utcnow()
            await self.session.commit()
            await self.session.refresh(user)
        return user
    
    async def increment_referral(self, referrer_id: int) -> Optional[User]:
        user = await self.get_by_telegram_id(referrer_id)
        if user:
            user.total_referrals += 1
            await self.session.commit()
            await self.session.refresh(user)
        return user
