from pydantic import BaseModel
from typing import List, Optional

# === Auth Schemas ===
class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str

# === Check Schemas ===
class CheckRequest(BaseModel):
    text: str

class CheckResponse(BaseModel):
    id: str
    status: str

class CheckStatusResponse(BaseModel):
    id: str
    status: str
    result: Optional[str] = None

# === History Schemas ===
class HistoryItem(BaseModel):
    id: str
    text_preview: str
    date: str
    status: str

# === Motor IA Schemas ===
class MotorIARequest(BaseModel):
    url: Optional[str] = None
    text: Optional[str] = None

class MotorIAResponse(BaseModel):
    score: int  # 0 a 100
    verdict: str  # "VERDADEIRO" ou "FALSO"
    explanation: str
    sources: List[str]  # Lista de URLs das fontes
