from pydantic import BaseModel, Field

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    project_id: int | None = None
    tags: list[str] = Field(default_factory=list, max_items=5)

class TaskUpdate(BaseModel):
    title: str | None = Field(None, min_length=3, max_length=100)
    is_completed: bool | None = None
    tags: list[str] | None = Field(None, max_items=5)

class TaskResponse(BaseModel):
    id: int
    title: str
    is_completed: bool
    tags: list[str]
    project_id: int | None