from fastapi import APIRouter, Depends, status
from app.core.database import get_db 
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.knight import KnightCreate, KnightResponse
from app.models.knight import Knight
from sqlalchemy import select
from app.core.security import get_current_user

knights_router = APIRouter(prefix="/knights", tags=["Knights"])

@knights_router.post("/", status_code=status.HTTP_201_CREATED, response_model=KnightResponse)
async def create_knight(knight: KnightCreate, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    new_knight = Knight(**knight.model_dump())
    db.add(new_knight)
    await db.commit()
    await db.refresh(new_knight)
    return new_knight

@knights_router.get("/", response_model=list[KnightResponse])
async def get_knights(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Knight))
    knights = result.scalars().all()
    return knights

