from pydantic import BaseModel, Field
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
    text: str = Field(
        ...,
        min_length=10,
        max_length=5000,
        description="Texto da notícia ou URL para análise"
    )


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
    text: str
    text_preview: Optional[str] = None
    date: str
    status: str
    result: Optional[str] = None
    created_at: Optional[str] = None
