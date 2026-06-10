from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel , Field
from typing import Annotated 

app = FastAPI(title="Practice")

def validate_squire(age: int):
    if age < 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Applicants must be at least 10 years old."
        )
    return age

class SquireApply(BaseModel):
    name : str = Field(..., description="Name of the applicant")
    age : Annotated[int, Depends(validate_squire), Field(..., description="Age of the applicant")]

class SquireResponse(SquireApply):
    id : int = Field(..., description="ID of the squire")
    message: str = Field(..., description="Application status message")
squires = []
curr_id = 1
@app.post("/squire/apply", status_code=status.HTTP_201_CREATED, response_model=SquireResponse)
def apply_squire(application: SquireApply):
    global curr_id
    squire_info = application.model_dump()
    squire = {
        "id" : curr_id,
        "message" : f"{squire_info['name']} is hired as a squire."
        **squire_info
    }
    curr_id += 1
    squires.append(squire)
    return squire