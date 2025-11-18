from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from database import SessionLocal
from models import User
from schemas import AccountStatus, FakeUpgradeRequest

router = APIRouter(prefix="/pro", tags=["billing"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/account/{user_id}", response_model=AccountStatus)
def get_account(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")
    return user

@router.post("/fake-upgrade")
def fake_upgrade(req: FakeUpgradeRequest, db: Session = Depends(get_db)):
    """
    Демо-апгрейд до PRO без реальної оплати.
    У проді тут буде інтеграція з Stripe/LiqPay/WayForPay.
    """
    user = db.query(User).filter(User.id == req.user_id).first()
    if not user:
        raise HTTPException(404, "User not found")

    user.is_pro = True
    user.pro_until = datetime.utcnow() + timedelta(days=30)
    db.commit()
    return {"ok": True, "pro_until": user.pro_until.isoformat()}
