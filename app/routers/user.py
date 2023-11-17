from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="../templates")

@router.get("/user/{username}", response_class=HTMLResponse, tags=["User"])
async def get_user(request: Request, username: str):
    return templates.TemplateResponse("user.html", {"request": request, "username": username})