from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel, Field
from typing import Annotated 

app = FastAPI(title="The Hedge Knight API")

# 1. The Pydantic Model (Pure Data Shape)
class SquireApply(BaseModel):
    name: str = Field(..., description="Name of the applicant")
    age: int = Field(..., description="Age of the applicant")

class SquireResponse(SquireApply):
    id: int
    message: str

# 2. The Dependency (Executes business logic on the data)
def validate_squire(squire: SquireApply):
    if squire.age < 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Applicants must be at least 10 years old."
        )
    return squire # Return the validated object

# 3. Create the Annotated Injection Type
ValidatedSquire = Annotated[SquireApply, Depends(validate_squire)]

squires = []
curr_id = 1

# 4. The Endpoint (Inject the dependency here)
@app.post("/squire/apply", status_code=status.HTTP_201_CREATED, response_model=SquireResponse)
def apply_squire(application: ValidatedSquire):
    global curr_id
    
    squire_info = application.model_dump()
    squire = {
        "id": curr_id,
        "message": f"{squire_info['name']} is hired as a squire.", # Comma added!
        **squire_info
    }
    
    curr_id += 1
    squires.append(squire)
    return squire