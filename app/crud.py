from sqlalchemy.orm import Session
from app import models, schemas


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
        return {"error": "Material not found"}

    # INCREASE STOCK
    if movement.type == "IN":
        material.quantity += movement.quantity

    # DECREASE STOCK
    elif movement.type == "OUT":
        material.quantity -= movement.quantity

        if material.quantity < 0:
            return {"error": "Not enough stock"}

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
