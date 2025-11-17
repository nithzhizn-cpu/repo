from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Message
from schemas import MessageCreate

router=APIRouter(prefix="/messages")

def get_db():
    db=SessionLocal()
    try: yield db
    finally: db.close()

@router.post("")
def send(msg:MessageCreate, db:Session=Depends(get_db)):
    m=Message(from_id=1,to_id=msg.to,ciphertext=msg.ciphertext,iv=msg.iv)
    db.add(m)
    db.commit()
    return {"ok":True}

@router.get("")
def get(peer_id:int, db:Session=Depends(get_db)):
    msgs=db.query(Message).filter(
        (Message.from_id==1) | (Message.to_id==1)
    ).all()
    return {"messages":[{"from_id":m.from_id,"ciphertext":m.ciphertext,"iv":m.iv,"created_at":str(m.created_at)}for m in msgs]}
