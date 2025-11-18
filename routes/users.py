from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from schemas import UserOut, UserCreate, AccountStatus
import secrets

router = APIRouter(prefix="/users", tags=["users"])


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
        raise HTTPException(status_code=400, detail="Username cannot be empty")

    existing = db.query(User).filter(User.username == username).first()
    if existing:
        if not existing.token:
            existing.token = secrets.token_hex(32)
            db.commit()
            db.refresh(existing)
        return existing

    token = secrets.token_hex(32)
    user = User(username=username, token=token)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/search", response_model=list[UserOut])
def search(query: str, db: Session = Depends(get_db)):
    q = query.strip()
    if not q:
        return []
    users = db.query(User).filter(User.username.ilike(f"%{q}%")).all()
    return users


@router.get("/account/status", response_model=AccountStatus)
def account_status(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
