"""
Database Session — Async SQLAlchemy with SQLite fallback
"""

import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from config.settings import settings

logger = logging.getLogger(__name__)

def get_async_url() -> str:
    """Convert DATABASE_URL to async format with SQLite fallback"""
    url = settings.DATABASE_URL
    
    # Check if empty or unresolved
    if not url or url == "" or url.startswith("${") or url.startswith("Postgres."):
        logger.warning("⚠️ DATABASE_URL unresolved — using SQLite fallback")
        url = "sqlite:///leakbot.db"
    
    # Convert to async format
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+asyncpg://", 1)
    elif url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql+asyncpg://", 1)
    elif url.startswith("sqlite:///"):
        return url.replace("sqlite:///", "sqlite+aiosqlite:///", 1)
    else:
        # Assume SQLite
        return "sqlite+aiosqlite:///leakbot.db"

def create_engine_with_fallback():
    """Create engine — SQLite doesn't support pool_size"""
    url = get_async_url()
    logger.info(f"📦 Using database: {url[:60]}...")
    
    # SQLite — no pool_size/max_overflow
    if "sqlite" in url:
        return create_async_engine(
            url,
            echo=False,
            connect_args={"check_same_thread": False},
        )
    
    # PostgreSQL — full pool config
    try:
        return create_async_engine(
            url,
            echo=False,
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,
            pool_recycle=3600,
        )
    except Exception as e:
        logger.error(f"❌ PostgreSQL engine failed: {e}")
        logger.info("🔄 Falling back to SQLite...")
        return create_async_engine(
            "sqlite+aiosqlite:///leakbot.db",
            echo=False,
            connect_args={"check_same_thread": False},
        )

# Create engine
engine = create_engine_with_fallback()

# Session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Base for models
Base = declarative_base()

async def init_db():
    """Initialize database — create tables"""
    logger.info("📦 Initializing database...")
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("✅ Database ready")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        raise

async def get_db():
    """Dependency for repositories"""
    async with AsyncSessionLocal() as session:
        yield session
