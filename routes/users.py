from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
import secrets

router=APIRouter(prefix="/users")

def get_db():
    db=SessionLocal()
    try: yield db
    finally: db.close()

@router.post("/register")
def register(data: dict, db: Session=Depends(get_db)):
    username=data["username"]
    user=User(username=username)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id":user.id,"username":user.username,"token":secrets.token_hex(16)}
