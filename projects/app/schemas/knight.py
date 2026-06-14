from pydantic import BaseModel, Field, ConfigDict 

class KnightBase(BaseModel):
    name: str = Field(..., max_length=50)
    sword_name: str | None = Field(None)

class KnightCreate(KnightBase):
    pass

class KnightResponse(KnightBase):
    id: int 
    is_kingsguard: bool
    model_config = ConfigDict(from_attributes=True)