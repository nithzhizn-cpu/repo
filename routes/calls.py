from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import CallSignal
from schemas import CallOffer, CallAnswer, Candidate

router = APIRouter(prefix="/call", tags=["call"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/offer")
def offer(data: CallOffer, db: Session = Depends(get_db)):
    c = CallSignal(from_id=1, to_id=data.to, type="offer", data=data.sdp)
    db.add(c)
    db.commit()
    return {"ok": True}


@router.post("/answer")
def answer(data: CallAnswer, db: Session = Depends(get_db)):
    c = CallSignal(from_id=1, to_id=data.to, type="answer", data=data.sdp)
    db.add(c)
    db.commit()
    return {"ok": True}


@router.post("/candidate")
def candidate(data: Candidate, db: Session = Depends(get_db)):
    c = CallSignal(from_id=1, to_id=data.to, type="candidate", data=data.candidate)
    db.add(c)
    db.commit()
    return {"ok": True}


@router.get("/poll")
def poll(db: Session = Depends(get_db)):
    c = db.query(CallSignal).all()
    return {
        "signals": [
            {
                "from_id": x.from_id,
                "type": x.type,
                "data": x.data
            } for x in c
        ]
    }
