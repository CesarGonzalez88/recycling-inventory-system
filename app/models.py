from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

# USERS


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# MATERIALS
class Material(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String)
    quantity = Column(Integer, default=0)
    unit = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    movements = relationship(
        "Movement",
        back_populates="material"
    )


# MOVEMENTS
class Movement(Base):
    __tablename__ = "movements"

    id = Column(Integer, primary_key=True, index=True)

    material_id = Column(Integer, ForeignKey("materials.id"))

    type = Column(String)  # IN / OUT
    quantity = Column(Integer)
    description = Column(String)

    material = relationship(
        "Material",
        back_populates="movements"
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())
