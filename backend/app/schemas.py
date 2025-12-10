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

class HistoryCreate(BaseModel):
    text: str
    result: str


class HistoryItem(BaseModel):
    id: str
    text_preview: str
    date: str
    status: str
