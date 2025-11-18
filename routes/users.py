from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from schemas import UserOut, UserCreate
import secrets

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ===========================
#  REGISTER USER
# ===========================
@router.post("/register", response_model=UserOut)
def register(data: UserCreate, db: Session = Depends(get_db)):
    username = data.username.strip()

    if not username:
        raise HTTPException(status_code=400, detail="Username cannot be empty")

    existing = db.query(User).filter(User.username == username).first()
    if existing:
        # Якщо користувач уже існує — додамо token якщо нема
        if not existing.token:
            existing.token = secrets.token_hex(32)
            db.commit()
        return existing

    # Створюємо нового юзера з токеном
    token = secrets.token_hex(32)
    user = User(username=username, token=token)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# ===========================
#  SEARCH USERS
# ===========================
@router.get("/search", response_model=list[UserOut])
def search(query: str, db: Session = Depends(get_db)):
    q = query.strip()

    users = db.query(User).filter(User.username.ilike(f"%{q}%")).all()
    return users     # Фронтенд ОЧІКУЄ СПИСОК, НЕ {"results": ...}
