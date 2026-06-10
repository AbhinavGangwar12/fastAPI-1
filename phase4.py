from fastapi import FastAPI, status, Depends, HTTPException
from typing import Annotated
import time

app = FastAPI(title="FastAPI Dependency Injection Example")

def check_knighthood(title: str = "Ser"):
    if title.lower() != "ser":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only anointed knights are allowed."
        )
    return title

KnightGuard = Annotated[str, Depends(check_knighthood)]

def get_tourney_tent():
    print("Setting up the tourney tent...")
    tent_inventory = ["lances", "shields", "horses", "armor"]
    yield tent_inventory
    print("Tearing down the tourney tent...")

TentDep = Annotated[list[str], Depends(get_tourney_tent)]

@app.get("/tourney/joust", status_code=status.HTTP_200_OK)
async def enter_joust(knight: KnightGuard, tent: TentDep):
    # if the knight doesn't pass ?title=Ser, the check_knighthood will raise a 403 error and this function won't execute.
    return {
        "message": f"Welcome to the joust, {knight}! The tent is stocked with: {', '.join(tent)}."
    }

"""
We can mix things up, type validation with dependency injection. In the pydantic models, we can use Annotated to specify that a certain field should be provided by a dependency. This allows us to have more complex logic for how certain values are obtained.
"""