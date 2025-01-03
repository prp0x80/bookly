from sqlmodel import create_engine, text
from sqlalchemy.ext.asyncio import AsyncEngine

from src.config import settings

engine = AsyncEngine(create_engine(url=settings.DATABASE_URL, echo=True))


async def init_db():
    async with engine.begin() as conn:
        statement = text("SELECT 'hello';")
        result = await conn.execute(statement)
        print(result.all())
