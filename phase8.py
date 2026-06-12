from fastapi import FastAPI, status, BackgroundTasks
import time
import asyncio

app = FastAPI(title="The Citadel API")

def forge_valyrian_steel(sword_name: str):
    print(f"Starting the fire for {sword_name}...")
    time.sleep(5)
    print(f"{sword_name} is fully forged!")

async def dispatch_raven(house: str, message: str):
    print(f"Raven taking flight to House {house}...")
    await asyncio.sleep(3)
    print(f"Message delivered to {house}: '{message}'")

@app.post("/blacksmith/forge", status_code=status.HTTP_202_ACCEPTED)
async def order_sword(sword_name: str, bg_task: BackgroundTasks):
    bg_task.add_task(forge_valyrian_steel, sword_name)
    return {"message": f"Your order for {sword_name} is being processed!"}

@app.post("/maester/message", status_code=status.HTTP_202_ACCEPTED)
async def send_message(house: str, message: str, bg_task: BackgroundTasks):
    bg_task.add_task(dispatch_raven, house, message)
    return {"message": f"Your message to House {house} is being delivered!"}

@app.get("/")
async def read_root():
    return {"message": "Welcome to The Citadel API! Forge swords and send ravens with ease."}