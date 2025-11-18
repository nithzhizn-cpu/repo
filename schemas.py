from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserOut(BaseModel):
    id: int
    username: str
    is_pro: bool = False

    class Config:
        orm_mode = True

class AccountStatus(BaseModel):
    id: int
    username: str
    is_pro: bool
    pro_until: Optional[datetime] = None

    class Config:
        orm_mode = True

class FakeUpgradeRequest(BaseModel):
    user_id: int

class UserCreate(BaseModel):
    username:str

class MessageCreate(BaseModel):
    to:int
    iv:str
    ciphertext:str

class CallOffer(BaseModel):
    to:int
    sdp:str

class CallAnswer(BaseModel):
    to:int
    sdp:str

class Candidate(BaseModel):
    to:int
    candidate:str
