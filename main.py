from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from database import Base, engine
from routes.users import router as users_router
from routes.messages import router as messages_router
from routes.calls import router as calls_router
from routes.billing import router as billing_router

# -------- DATABASE INIT --------
Base.metadata.create_all(bind=engine)

# -------- FASTAPI APP --------
app = FastAPI(title="SpySignal Premium Backend")

# -------- CORS --------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Можеш замінити на домен свого Railway
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------- STATIC FILES --------
# frontend доступний за https://yourapp.railway.app/
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def index():
    return FileResponse("static/index.html")

# -------- HEALTHCHECK --------
@app.get("/health")
def health():
    return {"status": "ok"}

# -------- API ROUTERS --------
app.include_router(users_router, prefix="/api")
app.include_router(messages_router, prefix="/api")
app.include_router(calls_router, prefix="/api")
app.include_router(billing_router, prefix="/api")

# -------- SECRET ONE-TIME RESET --------
ADMIN_RESET_KEY = os.getenv("ADMIN_RESET_KEY", "")
HAS_RESET = False  # блокує повторний reset


@app.get("/__internal_reset_db", include_in_schema=False)
def internal_reset(request: Request):
    """
    🔥 СЕКРЕТНИЙ reset БД.
    Працює ТІЛЬКИ якщо передати заголовок X-Admin-Key.
    Після першого запуску — блокується.
    Не показується в /docs.
    """

    global HAS_RESET

    if HAS_RESET:
        raise HTTPException(status_code=403, detail="Reset already used")

    key = request.headers.get("X-Admin-Key")
    if key != ADMIN_RESET_KEY or not key:
        raise HTTPException(status_code=403, detail="Unauthorized")

    removed = []
    for name in ["app.db", "database.db", "sql_app.db"]:
        if os.path.exists(name):
            os.remove(name)
            removed.append(name)

    HAS_RESET = True

    return {"status": "ok", "removed": removed}
