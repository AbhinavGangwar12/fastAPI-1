from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker 
from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True, pool_size=10, max_overflow=20, pool_recycle=3600, pool_pre_ping=True)

asyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, autocommit=False, autoflush=False)

async def get_db():
    async with asyncSessionLocal() as session:
        yield session
