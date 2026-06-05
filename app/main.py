from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app import models, schemas, crud
from app.database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Inventory System API Running"}


# CREATE MATERIAL
@app.post("/materials")
def create_material(material: schemas.MaterialCreate, db: Session = Depends(get_db)):
    return crud.create_material(db, material)


# GET ALL MATERIALS
@app.get("/materials")
def read_materials(db: Session = Depends(get_db)):
    return crud.get_materials(db)


@app.get("/materials/{id}")
def get_material(id: int, db: Session = Depends(get_db)):
    return db.query(models.Material).filter(models.Material.id == id).first()


@app.put("/materials/{id}")
def update_material(id: int, updated: schemas.MaterialCreate, db: Session = Depends(get_db)):
    material = db.query(models.Material).filter(
        models.Material.id == id).first()

    material.name = updated.name
    material.type = updated.type
    material.quantity = updated.quantity
    material.unit = updated.unit

    db.commit()
    db.refresh(material)
    return material


@app.delete("/materials/{id}")
def delete_material(id: int, db: Session = Depends(get_db)):
    material = db.query(models.Material).filter(
        models.Material.id == id).first()

    db.delete(material)
    db.commit()
    return {"message": "Material deleted"}


@app.post("/movements")
def create_movement(movement: schemas.MovementCreate, db: Session = Depends(get_db)):
    return crud.create_movement(db, movement)
