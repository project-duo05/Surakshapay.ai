from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class TransactionRequest(BaseModel):
    transaction_id: str
    user_id: int
    amount: float
    location: str
    merchant: str

class RiskResponse(BaseModel):
    transaction_id: str
    risk_score: float
    decision: str
    reasons: List[str]

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    role: str
