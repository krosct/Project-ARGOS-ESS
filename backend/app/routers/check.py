from fastapi import APIRouter, HTTPException
from app.schemas import CheckRequest, CheckResponse, CheckStatusResponse
from app.supa import supabase
import uuid
import logging

router = APIRouter(prefix="/api/check", tags=["check"])


@router.post("/", response_model=CheckResponse)
def submit_check(request: CheckRequest):
    rec_id = str(uuid.uuid4())
    try:
        data = {
            "id": rec_id,
            "text": request.text,
            "status": "ANALYSING",
        }
        resp = supabase.table("checks").insert(data).execute()
        if resp.data is None and resp.error:
            logging.error(f"Supabase insert error: {resp.error}")
            raise HTTPException(status_code=503, detail="Database unavailable")
    except HTTPException:
        raise
    except Exception:
        logging.exception("DB error on submit_check")
        raise HTTPException(status_code=503, detail="Database unavailable")
    return {"id": rec_id, "status": "ANALYSING"}


@router.get("/{check_id}", response_model=CheckStatusResponse)
def get_check_status(check_id: str):
    try:
        resp = (
            supabase.table("checks")
            .select("id,status,result")
            .eq("id", check_id)
            .limit(1)
            .single()
            .execute()
        )
        if resp.data is None and resp.error:
            if getattr(resp, "status_code", 200) == 404:
                raise HTTPException(status_code=404, detail="Check not found")
            logging.error(f"Supabase select error: {resp.error}")
            raise HTTPException(status_code=503, detail="Database unavailable")
        if not resp.data:
            raise HTTPException(status_code=404, detail="Check not found")
        rec = resp.data
        return {
            "id": rec.get("id"),
            "status": rec.get("status"),
            "result": rec.get("result"),
        }
    except HTTPException:
        raise
    except Exception:
        logging.exception("DB error on get_check_status")
        raise HTTPException(status_code=503, detail="Database unavailable")
