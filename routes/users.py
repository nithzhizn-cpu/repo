from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from schemas import UserOut
import secrets

router = APIRouter(prefix="/users")
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=UserOut)
def register(data: dict, db: Session = Depends(get_db)):
    username = data["username"]

    existing = db.query(User).filter(User.username == username).first()
    if existing:
        return existing

    user = User(username=username)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/search")
def search(query: str, db: Session = Depends(get_db)):
    q = query.strip()
    users = db.query(User).filter(User.username.ilike(f"%{q}%")).all()
    # Можеш зробити більш гнучкий пошук (id+username)
    return {"results": [UserOut.from_orm(u) for u in users]}
