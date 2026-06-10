from fastapi import FastAPI, status
from pydantic import BaseModel, Field

class HorseCreate(BaseModel):
    name: str = Field(..., description="The name of the horse")
    role: str = Field(..., description="The role of the horse")
    top_speed: float = Field(..., description="The top speed of the horse in km/h", gt=0)

class HorseResponse(HorseCreate):
    horse_id: int = Field(..., description="The unique identifier of the horse")

app = FastAPI(title="Horse API")
horses_db = []
horse_id = 1

@app.post("/horses", status_code=status.HTTP_201_CREATED, response_model=HorseResponse)
async def create_horse(horse: HorseCreate):
    global horse_id
    new_horse = horse.model_dump()
    horse_new = {
        "horse_id": horse_id,
        **new_horse
    }
    horses_db.append(horse_new)
    horse_id += 1
    return horse_new
