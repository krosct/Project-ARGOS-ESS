from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import check, auth, history

app = FastAPI(title="Projeto Argos")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar rotas
app.include_router(check.router)
app.include_router(auth.router)
app.include_router(history.router)
