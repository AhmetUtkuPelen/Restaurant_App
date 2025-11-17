import logging
import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Default to development if ENVIRONMENT is not set
ENV = os.getenv("ENVIRONMENT", "DEVELOPMENT").upper()

# Set database URL based on environment
if ENV == "DEVELOPMENT":
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./E-Commerce.db")
    # Sync URL for SQLAdmin (remove aiosqlite)
    SYNC_DATABASE_URL = DATABASE_URL.replace("sqlite+aiosqlite", "sqlite")
    logger.info(f"Using SQLite database at: {DATABASE_URL}")
else:
    SUPABASE_URL = os.getenv("SUPABASE_CONNECTION_URL")
    if not SUPABASE_URL:
        raise ValueError(
            "SUPABASE_CONNECTION_URL environment variable is required for non-development environments"
        )
    DATABASE_URL = SUPABASE_URL
    # For PostgreSQL, sync URL is the same but without +asyncpg
    SYNC_DATABASE_URL = SUPABASE_URL.replace("+asyncpg", "")
    logger.info("Using Supabase database")

try:
    # The async engine is the entry point to the database for API routes
    engine = create_async_engine(
        DATABASE_URL,
        echo=True if ENV == "DEVELOPMENT" else False,
        pool_pre_ping=True,
    )
    logger.info("Async database engine created successfully")
    
    # Sync engine for SQLAdmin
    sync_engine = create_engine(
        SYNC_DATABASE_URL,
        echo=True if ENV == "DEVELOPMENT" else False,
        pool_pre_ping=True,
    )
    logger.info("Sync database engine created successfully for SQLAdmin")
except Exception as e:
    logger.error(f"Failed to create database engine: {str(e)}")
    raise

# The async_sessionmaker creates new asynchronous session objects to interact with the database.
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,  # Important for async usage to prevent expired object errors.
)

# --- Declarative Base for Models ---
Base = declarative_base()


async def init_db():
    """
    Asynchronously create all database tables based on the models.
    This should be called once on application startup.
    """
    async with engine.begin() as conn:
        # In a production environment, you would likely use a migration tool like Alembic
        # instead of create_all.
        logger.info("Initializing database tables...")
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables initialized.")


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
