from sqlalchemy.orm import Session
from app import models, schemas
from fastapi import HTTPException
from sqlalchemy import func


def create_material(db: Session, material: schemas.MaterialCreate):
    db_material = models.Material(
        name=material.name,
        type=material.type,
        quantity=material.quantity,
        unit=material.unit
    )
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material


def get_materials(db: Session):
    return db.query(models.Material).all()


def create_movement(db: Session, movement: schemas.MovementCreate):
    material = db.query(models.Material).filter(
        models.Material.id == movement.material_id).first()

    if not material:
        raise HTTPException(
            status_code=404,
            detail="material not found"
        )

    # INCREASE STOCK
    if movement.type == "IN":
        material.quantity += movement.quantity

    # DECREASE STOCK

    elif movement.type == "OUT":

        if material.quantity < movement.quantity:
            raise HTTPException(
                status_code=400,
                detail="Not enough stock"
            )
        material.quantity -= movement.quantity

    db_movement = models.Movement(
        material_id=movement.material_id,
        type=movement.type,
        quantity=movement.quantity,
        description=movement.description
    )

    db.add(db_movement)
    db.commit()
    db.refresh(material)

    return db_movement

# GET MOVEMENTS HISTORY


def get_movements(db: Session):
    return db.query(models.Movement).order_by(models.Movement.created_at.desc()).all()


# GET SUMMARY OF INVENTORY
def get_inventory_summary(db: Session):
    total_materials = db.query(models.Material).count()

    total_stock = db.query(func.sum(models.Material.quantity)).scalar()

    movements_count = db.query(models.Movement).count()

    return {
        "total_materials": total_materials,
        "total_stock": total_stock or 0,
        "movements_count": movements_count
    }
