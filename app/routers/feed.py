from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="../templates")

@router.get("/feed", response_class=HTMLResponse, tags=["Feed"])
async def login_form(request: Request):
    return templates.TemplateResponse("feed.html", {"request": request})

# TODO: Create a POST endpoint for the post creation form at /feed

# TODO: Create a GET endpoint for the post details at /feed/{post_id}

# TODO: Create a PUT endpoint for the post edition form at /feed/{post_id}

# TODO: Create a DELETE endpoint for the post deletion form at /feed/{post_id}