from pydantic import BaseModel
from datetime import datetime
from typing import Any



class ArchitectureCreate(BaseModel):
    content: str


class ArchitectureResponse(BaseModel):
    id: int
    content: str
    response: Any
    created_at: datetime

    class Config:
        from_attributes = True
