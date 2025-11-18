from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from schemas import UserOut, UserCreate
import secrets

router = APIRouter(prefix="/users")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", response_model=UserOut)
def register(data: UserCreate, db: Session = Depends(get_db)):
    username = data.username.strip()

    if not username:
        raise HTTPException(status_code=400, detail="Username is empty")

    existing = db.query(User).filter(User.username == username).first()

    if existing:
        if not existing.token:
            existing.token = secrets.token_hex(32)
            db.commit()
        return existing

    # create new
    user = User(
        username=username,
        token=secrets.token_hex(32)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/search", response_model=list[UserOut])
def search(query: str, db: Session = Depends(get_db)):
    q = query.strip()
    users = db.query(User).filter(User.username.ilike(f"%{q}%")).all()
    return users
