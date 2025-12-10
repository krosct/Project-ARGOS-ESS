from fastapi import APIRouter
from app.schemas import LoginRequest, LoginResponse

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/login", response_model=LoginResponse)
def login(credentials: LoginRequest):
    return {
        "access_token": "exemplo_12345",
        "token_type": "bearer"
    }
