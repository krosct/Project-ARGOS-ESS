from fastapi import APIRouter, HTTPException
from typing import List, Optional
from app.schemas import HistoryItem
from app.supa import supabase
import logging
import json

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

@router.get("/{item_id}")
def get_history_item(item_id: str):
    """Retorna o item completo do histórico incluindo o resultado"""
    try:
        resp = (
            supabase
            .table("checks")
            .select("id,text,status,result,created_at")
            .eq("id", item_id)
            .limit(1)
            .single()
            .execute()
        )
        if resp.data is None and resp.error:
            if getattr(resp, 'status_code', 200) == 404:
                raise HTTPException(status_code=404, detail="Item not found")
            logging.error(f"Supabase select error: {resp.error}")
            raise HTTPException(status_code=503, detail="Database unavailable")
        if not resp.data:
            raise HTTPException(status_code=404, detail="Item not found")
        
        rec = resp.data
        result_data = None
        if rec.get("result"):
            try:
                result_data = json.loads(rec.get("result"))
            except (json.JSONDecodeError, TypeError):
                result_data = rec.get("result")
        
        return {
            "id": rec.get("id"),
            "text": rec.get("text", ""),
            "status": rec.get("status", ""),
            "result": result_data,
            "created_at": rec.get("created_at", ""),
        }
    except HTTPException:
        raise
    except Exception:
        logging.exception("DB error on get_history_item")
        raise HTTPException(status_code=503, detail="Database unavailable")

@router.delete("/{item_id}")
def delete_history_item(item_id: str):
    """Deleta um item do histórico"""
    try:
        resp = (
            supabase
            .table("checks")
            .delete()
            .eq("id", item_id)
            .execute()
        )
        if resp.data is None and resp.error:
            logging.error(f"Supabase delete error: {resp.error}")
            raise HTTPException(status_code=503, detail="Database unavailable")
        return {"message": "Item deletado com sucesso", "id": item_id}
    except HTTPException:
        raise
    except Exception:
        logging.exception("DB error on delete_history_item")
        raise HTTPException(status_code=503, detail="Database unavailable")

@router.delete("/clear")
def clear_history():
    """Limpa todo o histórico"""
    try:
        resp = (
            supabase
            .table("checks")
            .delete()
            .neq("id", "")  # Deleta todos os registros
            .execute()
        )
        if resp.data is None and resp.error:
            logging.error(f"Supabase clear error: {resp.error}")
            raise HTTPException(status_code=503, detail="Database unavailable")
        return {"message": "Histórico limpo com sucesso"}
    except HTTPException:
        raise
    except Exception:
        logging.exception("DB error on clear_history")
        raise HTTPException(status_code=503, detail="Database unavailable")
