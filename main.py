from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from database import Base, engine
from routes.users import router as users_router
from routes.messages import router as messages_router
from routes.calls import router as calls_router
from routes.billing import router as billing_router

# Створення таблиць
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SpySignal Premium Backend")

# CORS — потрібен для WebApp і HTML
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🚀 ВАЖЛИВО — МОНТУЄМО STATIC/
app.mount("/", StaticFiles(directory="static", html=True), name="static")

# API роутери
app.include_router(users_router, prefix="/api")
app.include_router(messages_router, prefix="/api")
app.include_router(calls_router, prefix="/api")
app.include_router(billing_router, prefix="/api")

# healthcheck
@app.get("/health")
def health():
    return {"status": "ok"}
