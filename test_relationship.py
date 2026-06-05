from app.database import SessionLocal
from app.models import Material

db = SessionLocal()

material = db.query(Material).first()

if material:
    print(material.name)

    for movement in material.movements:
        print(
            movement.type,
            movement.quantity
        )
else:
    print("No materials found")
