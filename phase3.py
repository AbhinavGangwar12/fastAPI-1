from fastapi import FastAPI, status
from pydantic import BaseModel, Field

app = FastAPI(title="The Hedge Knight API")

class SquireBase(BaseModel):
    name: str = Field(..., description="The name of the squire")
    age: int = Field(..., description="The age of the squire", gt=5, lt=80)

class SquireCreate(SquireBase):
    secret_fear: str = Field(..., description="The squire's secret fear")

class SquireResponse(SquireBase):
    id: int 
    is_knighted: bool = False

squire_db = []
current_id = 1

# response_model tells FastAPI what does the function returns.
@app.post("/squires", response_model=SquireResponse, status_code=status.HTTP_201_CREATED)
async def create_squire(squire: SquireCreate):
    global current_id 
    squire_data = squire.model_dump()
    new_squire = {
        "id": current_id,
        "is_knighted": False,
        **squire_data
    }
    squire_db.append(new_squire)
    current_id += 1
    return new_squire
