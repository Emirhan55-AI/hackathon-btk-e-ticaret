from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import NullPool
import logging

logger = logging.getLogger("app.core.database")

# Base class for SQLAlchemy models
Base = declarative_base()


class Database:
    """Database connection manager."""
    
    def __init__(self, url: str):
        self.url = url
        self.engine = None
        self.session_factory = None
        
    async def connect(self) -> None:
        """Initialize database connection."""
        try:
            # Create async engine
            self.engine = create_async_engine(
                self.url,
                echo=False,  # Set to True for SQL logging in development
                poolclass=NullPool,  # Use NullPool for async to avoid connection issues
                future=True,
            )
            
            # Create session factory
            self.session_factory = async_sessionmaker(
                bind=self.engine,
                class_=AsyncSession,
                expire_on_commit=False,
                autoflush=True,
                autocommit=False,
            )
            
            logger.info("Database connection initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize database connection: {e}")
            raise
    
    async def disconnect(self) -> None:
        """Close database connection."""
        try:
            if self.engine:
                await self.engine.dispose()
                logger.info("Database connection closed successfully")
        except Exception as e:
            logger.error(f"Error closing database connection: {e}")
    
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get database session."""
        if not self.session_factory:
            raise RuntimeError("Database not initialized. Call connect() first.")
        
        async with self.session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception as e:
                await session.rollback()
                logger.error(f"Database session error: {e}")
                raise
            finally:
                await session.close()


# Global database instance
database = Database("")


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting database session."""
    async for session in database.get_session():
        yield session


def init_database(database_url: str) -> Database:
    """Initialize database with given URL."""
    global database
    database = Database(database_url)
    return database
