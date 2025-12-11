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
            supabase.table("checks")
            .select("id,text,status,result,created_at")
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
                "text": r.get("text", ""),
                "text_preview": preview(r.get("text", "")),
                "date": (r.get("created_at", "")[:10] if r.get("created_at") else ""),
                "status": r.get("status", ""),
                "result": r.get("result"),
                "created_at": r.get("created_at"),
            }
            for r in rows
        ]
        return items
    except HTTPException:
        raise
    except Exception:
        logging.exception("DB error on get_history")
        raise HTTPException(status_code=503, detail="Database unavailable")


@router.get("/{item_id}", response_model=HistoryItem)
def get_history_item(item_id: str):
    try:
        resp = (
            supabase.table("checks")
            .select("id,text,status,result,created_at")
            .eq("id", item_id)
            .limit(1)
            .single()
            .execute()
        )
        if resp.data is None and resp.error:
            if getattr(resp, "status_code", 200) == 404:
                raise HTTPException(status_code=404, detail="History item not found")
            logging.error(f"Supabase select error: {resp.error}")
            raise HTTPException(status_code=503, detail="Database unavailable")
        if not resp.data:
            raise HTTPException(status_code=404, detail="History item not found")

        r = resp.data
        def preview(text: str, n: int = 60) -> str:
            return text if not text or len(text) <= n else text[:n] + "..."
        return {
            "id": r.get("id"),
            "text": r.get("text", ""),
            "text_preview": preview(r.get("text", "")),
            "date": (r.get("created_at", "")[:10] if r.get("created_at") else ""),
            "status": r.get("status", ""),
            "result": r.get("result"),
            "created_at": r.get("created_at"),
        }
    except HTTPException:
        raise
    except Exception:
        logging.exception("DB error on get_history_item")
        raise HTTPException(status_code=503, detail="Database unavailable")


@router.delete("/{item_id}")
def delete_history_item(item_id: str):
    try:
        resp = (
            supabase.table("checks")
            .delete()
            .eq("id", item_id)
            .execute()
        )
        if resp.data is None and resp.error:
            logging.error(f"Supabase delete error: {resp.error}")
            raise HTTPException(status_code=503, detail="Database unavailable")
        return {"message": "Item deletado com sucesso"}
    except HTTPException:
        raise
    except Exception:
        logging.exception("DB error on delete_history_item")
        raise HTTPException(status_code=503, detail="Database unavailable")


@router.delete("/clear")
def clear_history():
    try:
        # Deleta todos os registros completados ou falhados
        resp = (
            supabase.table("checks")
            .delete()
            .in_("status", ["COMPLETED", "FAILED"])
            .execute()
        )
        if resp.data is None and resp.error:
            logging.error(f"Supabase delete error: {resp.error}")
            raise HTTPException(status_code=503, detail="Database unavailable")
        return {"message": "Histórico limpo com sucesso"}
    except HTTPException:
        raise
    except Exception:
        logging.exception("DB error on clear_history")
        raise HTTPException(status_code=503, detail="Database unavailable")
