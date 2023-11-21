from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="../templates")

@router.get("/register", response_class=HTMLResponse, tags=["Register"])
async def register_form(request: Request ):
    return templates.TemplateResponse("register.html", {"request": request})


# TODO: Create a POST endpoint for the registration form