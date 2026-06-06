from datetime import datetime

from pydantic import BaseModel, Field
from typing import Literal, Optional


class MaterialBase(BaseModel):
    name: str
    type: str
    quantity: int
    unit: str


class MaterialCreate(BaseModel):
    name: str
    type: str
    quantity: int
    unit: str


class MaterialResponse(MaterialBase):
    id: int

    class Config:
        from_attributes = True


class MovementCreate(BaseModel):
    material_id: int
    type: Literal["IN", "OUT"]  # IN / OUT
    quantity: int = Field(gt=0)  # more than 0
    description: str


class MaterialUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    quantity: Optional[int] = None
    unit: Optional[str] = None


class MovementResponse(BaseModel):
    id: int
    type: str
    quantity: int
    description: str
    created_at: datetime
    material: MaterialResponse

    class Config:
        from_attributes = True
