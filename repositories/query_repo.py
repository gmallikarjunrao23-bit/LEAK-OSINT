"""
Query repository
"""

from typing import List
from models import Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func
from datetime import datetime, timedelta
from repositories.base import BaseRepository
from models.query import Query

class QueryRepository(BaseRepository[Query]):
    def __init__(self, session: AsyncSession):
        super().__init__(Query, session)
    
    async def create_query(self, user_id: int, target: str, target_type: str,
                          result: dict, coins_used: int = 1) -> Query:
        found_count = len(result.get("results", {})) if result else 0
        return await self.create(
            user_id=user_id,
            target=target,
            target_type=target_type,
            result=result,
            found_count=found_count,
            coins_used=coins_used
        )
    
    async def get_user_history(self, user_id: int, limit: int = 10) -> List[Query]:
        stmt = select(Query).filter_by(user_id=user_id).order_by(desc(Query.created_at)).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def get_user_stats(self, user_id: int) -> dict:
        total = await self.count(user_id=user_id)
        stmt = select(func.sum(Query.found_count)).filter_by(user_id=user_id)
        result = await self.session.execute(stmt)
        found_total = result.scalar() or 0
        return {"total_searches": total, "total_found": found_total}
    
    async def get_global_stats(self) -> dict:
        total = await self.count()
        stmt = select(func.sum(Query.found_count))
        result = await self.session.execute(stmt)
        found_total = result.scalar() or 0
        return {"total_searches": total, "total_found": found_total}
