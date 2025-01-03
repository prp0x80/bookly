from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.books.routes import book_router
from src.db.main import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application started")
    await init_db()
    yield
    print("Application stopped")


version = "v1"

app = FastAPI(title="Bookly",
              description="A REST API for a book review web service", version=version, lifespan=lifespan)

app.include_router(book_router, prefix=f"/api/{version}/books", tags=["books"])
