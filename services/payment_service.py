"""
Payment service — UPI with admin approval
"""

from models.payment import Payment
from typing import Optional, List, Dict, Any
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.payment_repo import PaymentRepository
from repositories.user_repo import UserRepository
from services.premium_service import PremiumService
from config.settings import settings

class PaymentService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.payment_repo = PaymentRepository(session)
        self.user_repo = UserRepository(session)
        self.premium_service = PremiumService(session)
    
    async def create_upi_payment(self, user_id: int, username: str, transaction_id: str,
                                 amount: float, plan: str, screenshot_url: str = None) -> Payment:
        return await self.payment_repo.create_payment(
            user_id=user_id,
            username=username,
            transaction_id=transaction_id,
            amount=amount,
            plan=plan,
            upi_id=settings.UPI_ID,
            screenshot_url=screenshot_url
        )
    
    async def approve_payment(self, payment_id: int, admin_id: int, notes: str = None) -> Dict[str, Any]:
        payment = await self.payment_repo.get_by_id(payment_id)
        if not payment:
            return {"success": False, "error": "Payment not found"}
        if payment.status != "pending":
            return {"success": False, "error": f"Payment already {payment.status}"}
        
        payment = await self.payment_repo.approve_payment(payment_id, admin_id, notes)
        
        if payment.plan == "premium":
            await self.premium_service.upgrade_to_premium(payment.user_id)
        elif payment.plan == "enterprise":
            await self.premium_service.upgrade_to_enterprise(payment.user_id)
        
        await self.payment_repo.complete_payment(payment_id)
        
        return {"success": True, "payment": payment}
    
    async def reject_payment(self, payment_id: int, admin_id: int, reason: str) -> Dict[str, Any]:
        payment = await self.payment_repo.get_by_id(payment_id)
        if not payment:
            return {"success": False, "error": "Payment not found"}
        if payment.status != "pending":
            return {"success": False, "error": f"Payment already {payment.status}"}
        
        payment = await self.payment_repo.reject_payment(payment_id, admin_id, reason)
        return {"success": True, "payment": payment}
    
    async def get_pending_payments(self) -> List[Payment]:
        return await self.payment_repo.get_pending_payments()
    
    async def get_user_payments(self, user_id: int, limit: int = 10) -> List[Payment]:
        return await self.payment_repo.get_user_payments(user_id, limit)
    
    async def get_payment_stats(self) -> dict:
        return await self.payment_repo.get_payment_stats()
