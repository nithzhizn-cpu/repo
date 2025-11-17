from pydantic import BaseModel

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
