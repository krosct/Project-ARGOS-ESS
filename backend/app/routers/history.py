from fastapi import APIRouter
from typing import List
from app.schemas import HistoryItem

router = APIRouter(prefix="/api/history", tags=["history"])

@router.get("/", response_model=List[HistoryItem])
def get_history():
    return [
        {
            "id": "1",
            "text": "Notícia sobre as eleições...",
            "result": "VERIFIED",
            "created_at": "2023-10-27"
        },
        {
            "id": "2",
            "text": "Tweet sobre as vacinas...",
            "result": "FAKE",
            "created_at": "2023-10-28"
        }
    ]
