from datetime import datetime

from pydantic import BaseModel, Field
from typing import Literal


class MaterialBase(BaseModel):
    name: str
    type: str
    quantity: int
    unit: str


class MaterialCreate(MaterialBase):
    pass


class MaterialResponse(MaterialBase):
    id: int

    class Config:
        from_attributes = True


class MovementCreate(BaseModel):
    material_id: int
    type: Literal["IN", "OUT"]  # IN / OUT
    quantity: int = Field(gt=0)  # more than 0
    description: str


class MovementResponse(BaseModel):
    id: int
    type: str
    quantity: int
    description: str
    created_at: datetime
    material: MaterialResponse

    class Config:
        from_attributes = True
