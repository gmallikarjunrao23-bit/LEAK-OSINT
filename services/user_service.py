"""
User service
"""

from typing import Optional, Tuple
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.user_repo import UserRepository
from repositories.query_repo import QueryRepository
from repositories.referral_repo import ReferralRepository
from config.settings import settings

class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository(session)
        self.query_repo = QueryRepository(session)
        self.referral_repo = ReferralRepository(session)
    
    async def get_or_create_user(self, telegram_id: int, first_name: str,
                                 username: str = None, last_name: str = None) -> User:
        user = await self.user_repo.get_by_telegram_id(telegram_id)
        if not user:
            user = await self.user_repo.create_user(
                telegram_id=telegram_id,
                first_name=first_name,
                username=username,
                last_name=last_name
            )
        return user
    
    async def get_user_with_details(self, telegram_id: int) -> dict:
        user = await self.user_repo.get_by_telegram_id(telegram_id)
        if not user:
            return None
        stats = await self.query_repo.get_user_stats(telegram_id)
        return {"user": user, "stats": stats}
    
    async def can_search(self, telegram_id: int) -> Tuple[bool, str]:
        user = await self.user_repo.get_by_telegram_id(telegram_id)
        if not user:
            return False, "User not found"
        if user.is_banned:
            return False, "🚫 You are banned"
        if user.coins < settings.COINS_PER_SEARCH:
            return False, "🪙 Insufficient coins. Use /plans or /refer."
        return True, "OK"
    
    async def perform_search(self, telegram_id: int, target: str, result: dict) -> dict:
        user = await self.user_repo.deduct_coins(telegram_id, settings.COINS_PER_SEARCH)
        if not user:
            return {"error": "Insufficient coins"}
        
        user = await self.user_repo.increment_searches(telegram_id)
        
        if not user.daily_reset_at or user.daily_reset_at < datetime.utcnow():
            user.daily_searches = 1
            user.daily_reset_at = datetime.utcnow()
        else:
            user.daily_searches += 1
        await self.session.commit()
        
        target_type = "phone" if target.replace('+', '').replace(' ', '').isdigit() else "email"
        query = await self.query_repo.create_query(
            user_id=telegram_id,
            target=target,
            target_type=target_type,
            result=result,
            coins_used=settings.COINS_PER_SEARCH
        )
        
        return {"user": user, "query": query}
    
    async def process_referral(self, referred_id: int, referral_code: str) -> Optional[dict]:
        existing = await self.referral_repo.get_by_referred(referred_id)
        if existing:
            return {"error": "Already used a referral code"}
        
        referrer = await self.user_repo.get_by_referral_code(referral_code)
        if not referrer:
            return {"error": "Invalid referral code"}
        if referrer.telegram_id == referred_id:
            return {"error": "Cannot refer yourself"}
        
        await self.referral_repo.create_referral(
            referrer_id=referrer.telegram_id,
            referred_id=referred_id,
            coins_awarded=settings.REFERRAL_REWARD_COINS
        )
        
        await self.user_repo.add_coins(referrer.telegram_id, settings.REFERRAL_REWARD_COINS)
        await self.user_repo.increment_referral(referrer.telegram_id)
        await self.user_repo.add_coins(referred_id, settings.REFERRAL_REWARD_COINS // 2)
        
        return {"success": True, "coins_awarded": settings.REFERRAL_REWARD_COINS}
