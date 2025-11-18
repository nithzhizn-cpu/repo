from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# ---------- USERS ----------
class UserOut(BaseModel):
    id: int
    username: str
    is_pro: bool = False

    model_config = {
        "from_attributes": True
    }


class AccountStatus(BaseModel):
    id: int
    username: str
    is_pro: bool
    pro_until: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }


class FakeUpgradeRequest(BaseModel):
    user_id: int


class UserCreate(BaseModel):
    username: str


# ---------- MESSAGES ----------
class MessageCreate(BaseModel):
    to: int
    iv: str
    ciphertext: str


# ---------- CALLS ----------
class CallOffer(BaseModel):
    to: int
    sdp: str


class CallAnswer(BaseModel):
    to: int
    sdp: str


class Candidate(BaseModel):
    to: int
    candidate: str
