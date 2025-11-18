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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1️⃣ API маршрути — завжди йдуть першими
app.include_router(users_router, prefix="/api")
app.include_router(messages_router, prefix="/api")
app.include_router(calls_router, prefix="/api")
app.include_router(billing_router, prefix="/api")

# 2️⃣ health-check (тепер працюватиме)
@app.get("/health")
def health_root():
    return {"status": "ok"}

@app.get("/api/health")
def health_api():
    return {"status": "ok"}

# 3️⃣ Головна сторінка — index.html
@app.get("/")
def serve_index():
    return FileResponse("static/index.html")

# 4️⃣ STATIC — монтуємо тільки на /static і ТІЛЬКИ ТУТ
app.mount("/static", StaticFiles(directory="static"), name="static")
