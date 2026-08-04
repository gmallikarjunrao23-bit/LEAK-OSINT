"""
Database Session — Async SQLAlchemy with SQLite fallback
"""

import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from config.settings import settings

logger = logging.getLogger(__name__)

def get_async_url() -> str:
    """
    Convert DATABASE_URL to async format.
    If URL is empty or unresolved, fallback to SQLite.
    """
    url = settings.DATABASE_URL
    
    # Check if empty, null, or unresolved variable reference
    if not url or url == "" or url.startswith("${") or url.startswith("Postgres."):
        logger.warning("⚠️ DATABASE_URL is empty or unresolved — using SQLite fallback")
        url = "sqlite:///leakbot.db"
    
    # Convert to async format
    if url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
    elif url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+asyncpg://", 1)
    elif url.startswith("sqlite:///"):
        url = url.replace("sqlite:///", "sqlite+aiosqlite:///", 1)
    else:
        # Any other URL, try to use as-is but add aiosqlite for sqlite
        if "sqlite" in url:
            url = url.replace("sqlite://", "sqlite+aiosqlite://", 1)
    
    return url

def create_engine_with_fallback():
    """Create engine with fallback to SQLite if main fails"""
    url = get_async_url()
    logger.info(f"📦 Using database: {url[:60]}...")
    
    try:
        engine = create_async_engine(
            url,
            echo=False,
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,
            pool_recycle=3600,
        )
        return engine
    except Exception as e:
        logger.error(f"❌ Failed to create engine: {e}")
        logger.info("🔄 Falling back to SQLite...")
        return create_async_engine(
            "sqlite+aiosqlite:///leakbot.db",
            echo=False,
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
    """Initialize database — create tables if not exist"""
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
