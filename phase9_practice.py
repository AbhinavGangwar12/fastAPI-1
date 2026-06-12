from fastapi import FastAPI, status, BackgroundTasks, Depends, HTTPException
import time
import asyncio
from pydantic import BaseModel 
from typing import Annotated

app = FastAPI(title="The Citadel API")

# --- 1. Background Tasks ---

def execute_grooming(name: str): # Renamed to avoid collision
    print(f"Starting to groom {name}...")
    time.sleep(5)
    print(f"{name} has been groomed!")

def update_ledger(name: str, stags: int):
    with open("ledger.txt", "a") as f:
        f.write(f"{name} paid {stags} stags for grooming.\n")

async def send_single_invite(house: str): # Handles ONE house
    print(f"🐦 Inviting House {house}...")
    await asyncio.sleep(1)
    print(f"📜 Invite delivered to House {house}!")

# --- 2. Schemas & Dependencies ---

class ValidateLedgerRequest(BaseModel):
    name: str
    stags: int

def valid_pay(req: ValidateLedgerRequest):
    if req.stags < 10:
        # Correctly raising an HTTPException!
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Payment must be at least 10 stags."
        )
    return req 

LedgerRequest = Annotated[ValidateLedgerRequest, Depends(valid_pay)]

class SendInvitesRequest(BaseModel):
    houses: list[str]

# --- 3. Endpoints ---

@app.post("/stables/groom", status_code=status.HTTP_202_ACCEPTED)
async def request_grooming(name: str, bg_task: BackgroundTasks): # Renamed endpoint
    bg_task.add_task(execute_grooming, name)
    return {"message": f"Grooming {name} has been scheduled."}

@app.post("/treasury/pay", status_code=status.HTTP_202_ACCEPTED) # 202 is better here!
async def pay_grooming(request: LedgerRequest, bg_task: BackgroundTasks):
    bg_task.add_task(update_ledger, request.name, request.stags)
    return {"message": f"Payment of {request.stags} stags processed."}

@app.post("/tourney/invitations", status_code=status.HTTP_202_ACCEPTED)
async def dispatch_all_invites(request: SendInvitesRequest, bg_task: BackgroundTasks):
    # This is how you stack multiple background tasks!
    for house in request.houses:
        bg_task.add_task(send_single_invite, house)
        
    return {"message": f"Dispatching ravens to {len(request.houses)} houses."}