from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas import HistoryItem
from app.supa import supabase
import logging

router = APIRouter(prefix="/api/history", tags=["history"])

@router.get("/", response_model=List[HistoryItem])
def get_history():
    try:
        # order by created_at desc, limit 100
        resp = (
            supabase
            .table("checks")
            .select("id,text,status,created_at")
            .order("created_at", desc=True)
            .limit(100)
            .execute()
        )
        if resp.data is None and resp.error:
            logging.error(f"Supabase select history error: {resp.error}")
            raise HTTPException(status_code=503, detail="Database unavailable")
        rows = resp.data or []
        def preview(text: str, n: int = 60) -> str:
            return text if not text or len(text) <= n else text[:n] + "..."
        items = [
            {
                "id": r.get("id"),
                "text_preview": preview(r.get("text", "")),
                "date": (r.get("created_at", "")[:10] if r.get("created_at") else ""),
                "status": r.get("status", ""),
            }
            for r in rows
        ]
        return items
    except HTTPException:
        raise
    except Exception:
        logging.exception("DB error on get_history")
        raise HTTPException(status_code=503, detail="Database unavailable")
