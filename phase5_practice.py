from fastapi import FastAPI, status, Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import Annotated
from pydantic import BaseModel

DB_URL = "postgresql+asyncpg://abhi:abhi@localhost/practice_db"
engine = create_async_engine(DB_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass
class TourneyDB(Base):
    __tablename__ = "tourneys"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    location: Mapped[str] = mapped_column(nullable=False)
    prize_money: Mapped[int] = mapped_column(nullable=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
DBDep = Annotated[AsyncSession, Depends(get_db)]

class TourneyCreate(BaseModel):
    location: str
    prize_money: int

def validate_tourney(tourney: TourneyCreate):
    if tourney.prize_money < 0:
        raise ValueError("Prize money cannot be negative")
    return tourney

ValidatedTourney = Annotated[TourneyCreate, Depends(validate_tourney)]
app = FastAPI()
@app.post("/tourneys", status_code=status.HTTP_201_CREATED)
async def create_tourney(tourney: ValidatedTourney, db: DBDep):
    new_tourney = TourneyDB(location=tourney.location, prize_money=tourney.prize_money)
    db.add(new_tourney)
    await db.commit()
    await db.refresh(new_tourney)
    return {"id": new_tourney.id, "location": new_tourney.location, "prize_money": new_tourney.prize_money}
