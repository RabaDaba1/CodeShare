from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/login", response_class=HTMLResponse, tags=["Login"])
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})