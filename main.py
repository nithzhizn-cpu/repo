from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from database import Base, engine
from routes.users import router as users_router
from routes.messages import router as messages_router
from routes.calls import router as calls_router
from routes.billing import router as billing_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SpySignal Premium Backend")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# API маршрути (мають бути першими!)
# -------------------------
app.include_router(users_router, prefix="/api")
app.include_router(messages_router, prefix="/api")
app.include_router(calls_router, prefix="/api")
app.include_router(billing_router, prefix="/api")

# -------------------------
# HEALTHCHECK
# -------------------------
@app.get("/health")
def root_health():
    return {"status": "ok"}

@app.get("/api/health")
def api_health():
    return {"status": "ok"}

# -------------------------
# ГОЛОВНА СТОРІНКА
# -------------------------
@app.get("/")
def root():
    return FileResponse("static/index.html")

# -------------------------
# STATIC — монтуємо тільки на /static
# -------------------------
app.mount("/static", StaticFiles(directory="static"), name="static")
