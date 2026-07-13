from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.router import api_router


app = FastAPI(
    title="Youssef Portfolio AI",
    description="AI Portfolio Assistant",
    version="1.0.0"
)

# Static Files
app.mount("/static", StaticFiles(directory="static"), name="static")

# API Router
app.include_router(api_router)