from fastapi import APIRouter, BackgroundTasks, status 
import asyncio

ravens_router = APIRouter(prefix="/ravens", tags=["Ravens"])

async def fly_raven(house: str, message: str):
    await asyncio.sleep(3)
    print(f"Raven from {house} delivered message: {message}")
    return 

@ravens_router.post("/dispatch", status_code=status.HTTP_202_ACCEPTED)
async def dispatch_raven(house: str, message: str, bg_tasks: BackgroundTasks):
    bg_tasks.add_task(fly_raven, house, message)
    return {"detail": "Raven dispatched to deliver your message!"}