"""
Premium service
"""

from enum import Enum
from typing import Optional, Dict, Any
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.user_repo import UserRepository
from config.settings import settings

class PremiumTier(Enum):
    FREE = "free"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"

class PremiumService:
    FEATURES = {
        PremiumTier.FREE: {
            "max_daily_searches": 5,
            "export_pdf": False,
            "animated_emojis": False,
            "colored_buttons": False
        },
        PremiumTier.PREMIUM: {
            "max_daily_searches": 100,
            "export_pdf": True,
            "animated_emojis": True,
            "colored_buttons": True
        },
        PremiumTier.ENTERPRISE: {
            "max_daily_searches": 9999,
            "export_pdf": True,
            "animated_emojis": True,
            "colored_buttons": True
        }
    }
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository(session)
    
    @staticmethod
    def can_access(tier: str, feature: str) -> bool:
        tier_enum = PremiumTier(tier) if tier in [p.value for p in PremiumTier] else PremiumTier.FREE
        return PremiumService.FEATURES.get(tier_enum, {}).get(feature, False)
    
    async def get_user_tier(self, telegram_id: int) -> PremiumTier:
        user = await self.user_repo.get_by_telegram_id(telegram_id)
        if not user:
            return PremiumTier.FREE
        if user.is_premium and user.premium_expires_at and user.premium_expires_at < datetime.utcnow():
            user.is_premium = False
            user.plan = "free"
            await self.session.commit()
            return PremiumTier.FREE
        return PremiumTier(user.plan) if user.plan in [p.value for p in PremiumTier] else PremiumTier.FREE
    
    async def upgrade_to_premium(self, telegram_id: int) -> bool:
        user = await self.user_repo.set_premium(telegram_id, settings.PREMIUM_DAYS)
        return user is not None
    
    async def upgrade_to_enterprise(self, telegram_id: int) -> bool:
        user = await self.user_repo.set_enterprise(telegram_id, settings.ENTERPRISE_DAYS)
        return user is not None
    
    def get_pricing(self) -> dict:
        return {
            "premium": {"price": settings.PREMIUM_PRICE, "days": settings.PREMIUM_DAYS},
            "enterprise": {"price": settings.ENTERPRISE_PRICE, "days": settings.ENTERPRISE_DAYS}
        }
