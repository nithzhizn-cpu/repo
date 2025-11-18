from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__='users'
    id=Column(Integer, primary_key=True, index=True)
    username=Column(String, unique=True)
    # NEW:
    is_pro = Column(Boolean, default=False)
    pro_until = Column(DateTime, nullable=True)

class Message(Base):
    __tablename__='messages'
    id=Column(Integer, primary_key=True, index=True)
    from_id=Column(Integer)
    to_id=Column(Integer)
    ciphertext=Column(Text)
    iv=Column(Text)
    created_at=Column(DateTime, default=func.now())

class CallSignal(Base):
    __tablename__='calls'
    id=Column(Integer, primary_key=True, index=True)
    from_id=Column(Integer)
    to_id=Column(Integer)
    type=Column(String)
    data=Column(Text)
    created_at=Column(DateTime, default=func.now())
