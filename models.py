from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.sql import func
from database import Base

class User(Base):
    tablename = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    token = Column(String, unique=True, index=True)   # важливо!
    is_pro = Column(Boolean, default=False)
    pro_until = Column(DateTime, nullable=True)


class Message(Base):
    tablename = "messages"

    id = Column(Integer, primary_key=True, index=True)
    from_id = Column(Integer, index=True)
    to_id = Column(Integer, index=True)
    ciphertext = Column(Text)
    iv = Column(Text)
    created_at = Column(DateTime, server_default=func.now())


class CallSignal(Base):
    tablename = "calls"

    id = Column(Integer, primary_key=True, index=True)
    from_id = Column(Integer, index=True)
    to_id = Column(Integer, index=True)
    type = Column(String)
    data = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
