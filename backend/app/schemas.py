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
        description="Texto da notícia para análise"
    )


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
