from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import check, auth, history
from app.database import engine, Base
from app import models
import time
import logging
import os

# --- Inicialização do Banco com Retry (mantido da sua versão local) ---
if os.getenv("SUPABASE_HTTP", "0") != "1":
    _max_attempts = 5
    for attempt in range(1, _max_attempts + 1):
        try:
            models.Base.metadata.create_all(bind=engine)
            break
        except Exception as e:
            wait = min(2**attempt, 30)
            logging.warning(
                f"DB init attempt {attempt}/{_max_attempts} failed: {e}. Retrying in {wait}s..."
            )
            if attempt == _max_attempts:
                logging.error(
                    "DB initialization failed after retries; continuing to start API. \
                    Endpoints may fail until DB is reachable."
                )
                break
            time.sleep(wait)


app = FastAPI(title="Projeto Argos")


allowed_origins_str = \
    os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000")
origins = allowed_origins_str.split(",")


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(check.router)
app.include_router(auth.router)
app.include_router(history.router)


# --- Endpoint raiz (mantido da sua versão local) ---
@app.get("/")
def root():
    return {"message": "API is running"}

