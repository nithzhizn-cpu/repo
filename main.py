from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from routes.users import router as users_router
from routes.messages import router as messages_router
from routes.calls import router as calls_router
from routes.billing import router as billing_router

from database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Static
app.mount("/", StaticFiles(directory="static", html=True), name="static")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(users_router, prefix="/api/users")
app.include_router(messages_router, prefix="/api/messages")
app.include_router(calls_router, prefix="/api/calls")
app.include_router(billing_router, prefix="/api/billing")
