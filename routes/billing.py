from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from schemas import FakeUpgradeRequest, AccountStatus
from datetime import datetime, timedelta
from fastapi import HTTPException

router = APIRouter(prefix="/billing", tags=["billing"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/upgrade_fake", response_model=AccountStatus)
def upgrade_fake(data: FakeUpgradeRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_pro = True
    user.pro_until = datetime.utcnow() + timedelta(days=30)
    db.commit()
    db.refresh(user)
    return user
