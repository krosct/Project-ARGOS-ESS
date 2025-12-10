from fastapi import APIRouter, HTTPException
from app.schemas import CheckRequest, CheckResponse, CheckStatusResponse, CheckAnalysisResponse, NewsAnalysisResult
from app.supa import supabase
from app.services.gemini_service import analyze_news_with_gemini, extract_text_from_url
import uuid
import logging
import json

router = APIRouter(prefix="/api/check", tags=["check"])

@router.post("/", response_model=CheckAnalysisResponse)
def submit_check(request: CheckRequest):
    rec_id = str(uuid.uuid4())
    
    if not request.text and not request.url:
        raise HTTPException(status_code=400, detail="É necessário fornecer 'text' ou 'url'")
    
    # Extrair o texto da notícia
    news_text = ""
    if request.url:
        try:
            news_text = extract_text_from_url(request.url)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            logging.exception(f"Erro ao extrair conteúdo da URL: {e}")
            raise HTTPException(status_code=500, detail="Erro ao processar URL")
    else:
        news_text = request.text
    
    if not news_text or len(news_text.strip()) == 0:
        raise HTTPException(status_code=400, detail="O texto da notícia não pode estar vazio")
    
    # Salvar registro no banco de dados
    try:
        data = {
            "id": rec_id,
            "text": news_text[:500] if len(news_text) > 500 else news_text,
            "status": "ANALYSING",
            "result": None,
        }
        resp = supabase.table("checks").insert(data).execute()
        if resp.data is None and resp.error:
            logging.error(f"Supabase insert error: {resp.error}")
            raise HTTPException(status_code=503, detail="Database unavailable")
    except HTTPException:
        raise
    except Exception as e:
        logging.exception("DB error on submit_check")
        raise HTTPException(status_code=503, detail="Database unavailable")
    
    # Processar com Gemini
    try:
        analysis_result = analyze_news_with_gemini(news_text)
        
        # Salvar resultado no banco de dados
        result_json = json.dumps(analysis_result, ensure_ascii=False)
        try:
            supabase.table("checks").update({
                "status": "COMPLETED",
                "result": result_json
            }).eq("id", rec_id).execute()
        except Exception as e:
            logging.warning(f"Erro ao atualizar resultado no banco: {e}")
        
        return CheckAnalysisResponse(
            id=rec_id,
            status="COMPLETED",
            result=NewsAnalysisResult(
                score=analysis_result["score"],
                veredito=analysis_result["veredito"],
                explicacao=analysis_result["explicacao"],
                fontes=analysis_result["fontes"]
            )
        )
        
    except ValueError as e:
        error_status = "ERROR"
        error_result = json.dumps({"error": str(e)}, ensure_ascii=False)
        try:
            supabase.table("checks").update({
                "status": error_status,
                "result": error_result
            }).eq("id", rec_id).execute()
        except Exception:
            pass
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logging.exception(f"Erro ao processar com Gemini: {e}")
        error_status = "ERROR"
        error_result = json.dumps({"error": "Erro ao processar análise"}, ensure_ascii=False)
        try:
            supabase.table("checks").update({
                "status": error_status,
                "result": error_result
            }).eq("id", rec_id).execute()
        except Exception:
            pass
        raise HTTPException(status_code=500, detail="Erro ao processar análise da notícia")

@router.get("/{check_id}", response_model=CheckStatusResponse)
def get_check_status(check_id: str):
    try:
        resp = supabase.table("checks").select("id,status,result").eq("id", check_id).limit(1).single().execute()
        if resp.data is None and resp.error:
            if getattr(resp, 'status_code', 200) == 404:
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
