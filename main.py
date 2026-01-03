import os
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import engine, SessionLocal
from models import Base, TestItem

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def health():
    return {
        "status": "ok",
        "env_port": os.getenv("PORT"),
    }

@app.post("/items/{name}")
def create_item(name: str, db: Session = Depends(get_db)):
    item = TestItem(name=name)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@app.get("/items")
def list_items(db: Session = Depends(get_db)):
    return db.query(TestItem).all()

@app.delete("/items/{id}")
def delete_item(id: int, db: Session = Depends(get_db)):
    item = db.get(TestItem, id)
    db.delete(item)
    db.commit()
    if db.get(TestItem, id) is not None:
        return {"success": False, "message": "Falha ao tentar remover item"}
    return {"success": True, "message": "Item removido com sucesso."}
