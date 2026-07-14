from fastapi import APIRouter

from app.api.routes.portfolio import router as portfolio_router
from app.api.routes.voice import router as voice_router


api_router = APIRouter()

api_router.include_router(
    portfolio_router,
    tags=["Portfolio"]
)


api_router.include_router(voice_router)
