from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.schemas import CheckRequest, CheckResponse, CheckStatusResponse
from app.supa import supabase
from app.gemini_service import process_check
import uuid
import logging

router = APIRouter(prefix="/api/check", tags=["check"])


async def process_check_background(check_id: str, text_or_url: str):
    try:
        # Processa com Gemini
        result = await process_check(text_or_url)
        
        # Atualiza o registro no banco de dados
        update_data = {
            "status": "COMPLETED",
            "result": result,
        }
        resp = (
            supabase.table("checks")
            .update(update_data)
            .eq("id", check_id)
            .execute()
        )
        
        if resp.data is None and resp.error:
            logging.error(f"Supabase update error: {resp.error}")
    except Exception as e:
        logging.exception(f"Erro ao processar checagem {check_id}: {e}")
        try:
            supabase.table("checks").update({
                "status": "FAILED",
                "result": f"Erro ao processar: {str(e)}"
            }).eq("id", check_id).execute()
        except Exception:
            pass


@router.post("/", response_model=CheckResponse)
async def submit_check(request: CheckRequest, background_tasks: BackgroundTasks):
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
        
        # Inicia processamento em background
        # BackgroundTasks do FastAPI suporta corrotinas async diretamente
        background_tasks.add_task(process_check_background, rec_id, request.text)
        
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
