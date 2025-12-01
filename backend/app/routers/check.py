from fastapi import APIRouter
from app.schemas import CheckRequest, CheckResponse, CheckStatusResponse
import uuid

router = APIRouter(prefix="/api/check", tags=["check"])

@router.post("/", response_model=CheckResponse)
def submit_check(request: CheckRequest):
    fake_id = str(uuid.uuid4())
    
    # db_check = models.CheckRecord(id=fake_id, text=request.text)
    # db.add(db_check); db.commit()
    
    return {"id": fake_id, "status": "ANALYSING"}

@router.get("/{check_id}", response_model=CheckStatusResponse)
def get_check_status(check_id: str):
    return {
        "id": check_id,
        "status": "COMPLETED",
        "result": "Fake News detectada"
    }
