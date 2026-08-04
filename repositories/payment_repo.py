"""
Payment repository
"""

from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func
from repositories.base import BaseRepository
from models.payment import Payment

class PaymentRepository(BaseRepository[Payment]):
    def __init__(self, session: AsyncSession):
        super().__init__(Payment, session)
    
    async def create_payment(self, user_id: int, username: str, transaction_id: str,
                            amount: float, plan: str, upi_id: str,
                            screenshot_url: str = None) -> Payment:
        return await self.create(
            user_id=user_id,
            username=username,
            transaction_id=transaction_id,
            amount=amount,
            plan=plan,
            upi_id=upi_id,
            screenshot_url=screenshot_url,
            status="pending"
        )
    
    async def get_user_payments(self, user_id: int, limit: int = 10) -> List[Payment]:
        stmt = select(Payment).filter_by(user_id=user_id).order_by(desc(Payment.created_at)).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def get_pending_payments(self) -> List[Payment]:
        return await self.get_all(status="pending")
    
    async def approve_payment(self, payment_id: int, admin_id: int, notes: str = None) -> Optional[Payment]:
        from datetime import datetime
        payment = await self.get_by_id(payment_id)
        if payment:
            payment.status = "approved"
            payment.admin_id = admin_id
            payment.admin_notes = notes
            payment.reviewed_at = datetime.utcnow()
            await self.session.commit()
            await self.session.refresh(payment)
        return payment
    
    async def reject_payment(self, payment_id: int, admin_id: int, reason: str) -> Optional[Payment]:
        from datetime import datetime
        payment = await self.get_by_id(payment_id)
        if payment:
            payment.status = "rejected"
            payment.admin_id = admin_id
            payment.admin_notes = reason
            payment.reviewed_at = datetime.utcnow()
            await self.session.commit()
            await self.session.refresh(payment)
        return payment
    
    async def complete_payment(self, payment_id: int) -> Optional[Payment]:
        from datetime import datetime
        payment = await self.get_by_id(payment_id)
        if payment:
            payment.status = "completed"
            payment.completed_at = datetime.utcnow()
            await self.session.commit()
            await self.session.refresh(payment)
        return payment
    
    async def get_payment_stats(self) -> dict:
        total = await self.count()
        pending = await self.count(status="pending")
        completed = await self.count(status="completed")
        rejected = await self.count(status="rejected")
        return {"total": total, "pending": pending, "completed": completed, "rejected": rejected}
