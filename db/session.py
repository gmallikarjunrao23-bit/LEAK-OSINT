"""
Database Session — Async SQLAlchemy
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool
from config.settings import settings
import logging

logger = logging.getLogger(__name__)

def get_async_url() -> str:
    url = settings.DATABASE_URL
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+asyncpg://", 1)
    elif url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql+asyncpg://", 1)
    return url.replace("sqlite:///", "sqlite+aiosqlite:///", 1)

DATABASE_URL = get_async_url()

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()

async def init_db():
    logger.info("📦 Initializing database...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("✅ Database ready")

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
