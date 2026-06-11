from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import Annotated

DB_URL = "postgresql+asyncpg://abhi:abhi@localhost/practice_db"

engine = create_async_engine(DB_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    pass
class KnightDB(Base):
    __tablename__ = "knights"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(index=True)
    is_hedge_knight: Mapped[bool] = mapped_column(default=True)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

DBDep = Annotated[AsyncSession, Depends(get_db)]
app = FastAPI()

@app.post("/knights")
async def register_knight(name: str, db: DBDep):
    knight = KnightDB(name=name, is_hedge_knight=True)
    db.add(knight)
    await db.commit()
    await db.refresh(knight)
    return {"id": knight.id, "name": knight.name, "is_hedge_knight": knight.is_hedge_knight}

