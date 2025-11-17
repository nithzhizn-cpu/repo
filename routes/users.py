from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
import secrets

router = APIRouter(prefix="/users", tags=["users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------------
#  REGISTER ( /api/users/register )
# -------------------------------

@router.post("/register")
def register(data: dict, db: Session = Depends(get_db)):
    username = data["username"].strip()

    if not username:
        raise HTTPException(status_code=400, detail="Username required")

    # Перевірка чи існує вже
    existing = db.query(User).filter(User.username == username).first()
    if existing:
        return {
            "id": existing.id,
            "username": existing.username,
            "token": secrets.token_hex(16)
        }

    user = User(username=username)
    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "id": user.id,
        "username": user.username,
        "token": secrets.token_hex(16)
    }


# ------------------------------------
#  SEARCH USERS ( /api/users/search )
# ------------------------------------

@router.get("/search")
def search_users(query: str, db: Session = Depends(get_db)):
    q = query.strip()

    results = db.query(User).filter(
        (User.username.ilike(f"%{q}%")) |
        (User.id == q)
    ).all()

    return {"results": results}
