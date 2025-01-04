from sqlmodel import create_engine, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

from src.config import settings

async_engine = AsyncEngine(create_engine(url=settings.DATABASE_URL, echo=True))

# Create a sessionmaker for AsyncSession
async_session_maker = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)


async def init_db():
    async with async_engine.begin() as conn:
        from src.books.models import Book

        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session
