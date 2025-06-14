from pydantic import BaseModel, Field

class ProjectCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: str = Field("", max_length=500)

class ProjectResponse(BaseModel):
    id: int
    title: str
    description: str
    is_active: bool