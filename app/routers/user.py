from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="../templates")

@router.get("/user/{login}", response_class=HTMLResponse, tags=["User"])
async def get_user(request: Request, login: str):
    # TODO
    # Get user data from the database
    return templates.TemplateResponse("user.html", {"request": request, "login": login})