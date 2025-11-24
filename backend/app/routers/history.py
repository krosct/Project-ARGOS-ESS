from fastapi import APIRouter
from typing import List
from app.schemas import HistoryItem

router = APIRouter(prefix="/api/history", tags=["history"])

@router.get("/", response_model=List[HistoryItem])
def get_history():
    return [
        {
            "id": "1",
            "text_preview": "Notícia sobre as eleições...",
            "date": "2023-10-27",
            "status": "VERIFIED"
        },
        {
            "id": "2",
            "text_preview": "Tweet sobre as vacinas...",
            "date": "2023-10-28",
            "status": "FAKE"
        }
    ]
