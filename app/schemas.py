from pydantic import BaseModel


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
    type: str  # IN / OUT
    quantity: int
    description: str


class MovementResponse(BaseModel):
    id: int
    type: str
    quantity: int
    description: str
    material: MaterialResponse

    class Config:
        from_attributes = True
