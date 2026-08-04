"""
Database Session — SQLite fallback
"""

import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from config.settings import settings

logger = logging.getLogger(__name__)

def get_async_url() -> str:
    url = settings.DATABASE_URL
    
    if not url or url == "" or url.startswith("${") or url.startswith("Postgres."):
        logger.warning("⚠️ DATABASE_URL unresolved — using SQLite fallback")
        url = "sqlite:///leakbot.db"
    
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+asyncpg://", 1)
    elif url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql+asyncpg://", 1)
    else:
        return "sqlite+aiosqlite:///leakbot.db"

DATABASE_URL = get_async_url()
logger.info(f"📦 Using database: {DATABASE_URL[:50]}...")

# SQLite only — no pool_size
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
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
