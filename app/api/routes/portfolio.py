from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/portfolio")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )