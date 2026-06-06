from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app import models, schemas, crud
from app.database import engine, get_db
from app.schemas import MovementResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # luego lo restringimos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def serve_frontend():
    return FileResponse("frontend/frontend.html")


# CREATE MATERIAL
@app.post("/materials")
def create_material(material: schemas.MaterialCreate, db: Session = Depends(get_db)):
    return crud.create_material(db, material)


# GET ALL MATERIALS
@app.get("/materials")
def read_materials(db: Session = Depends(get_db)):

    data = crud.get_materials(db)

    return {
        "success": True,
        "data": data
    }


@app.get("/materials/{id}")
def get_material(id: int, db: Session = Depends(get_db)):

    data = db.query(models.Material).filter(models.Material.id == id).first()

    return {
        "success": True,
        "data": data
    }


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

    data = crud.create_movement(db, movement)

    return {
        "success": True,
        "data": data
    }


@app.get("/movements")
def read_movements(
    type: str = None,
    material_id: int = None,
    db: Session = Depends(get_db)
):
    data = crud.get_movements(db, type, material_id)

    return {
        "success": True,
        "data": data
    }


@app.get("/inventory-summary")
def inventory_summary(db: Session = Depends(get_db)):

    data = crud.get_inventory_summary(db)

    return {
        "success": True,
        "data": data
    }
