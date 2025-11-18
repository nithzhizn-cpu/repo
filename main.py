from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from routes.users import router as users_router
from routes.messages import router as messages_router
from routes.calls import router as calls_router
from routes.billing import router as billing_router

# Створення таблиць у базі
Base.metadata.create_all(bind=engine)

# Ініціалізація FastAPI
app = FastAPI(title="SpySignal Premium Backend")

# CORS — потрібен для WebApp і фронтенду
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # можна обмежити конкретним доменом
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Підключення роутів
app.include_router(users_router, prefix="/api")
app.include_router(messages_router, prefix="/api")
app.include_router(calls_router, prefix="/api")
app.include_router(billing_router, prefix="/api")

# Стандартний healthcheck
@app.get("/health")
def health():
    return {"status": "ok"}

# Головна сторінка, щоб не було 404 на /
@app.get("/")
def home():
    return {"message": "SpySignal backend is running"}
