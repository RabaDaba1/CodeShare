from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="../templates")

@router.get("/feed", response_class=HTMLResponse, tags=["Feed"])
async def feed(request: Request):
    return templates.TemplateResponse("feed.html", {"request": request})

@router.get("/feed/{post_id}", response_class=HTMLResponse, tags=["Feed"])
async def post_detailed(request: Request, post_id: int):
    # TODO: Get the post from the database and pass it to the template
    return templates.TemplateResponse("post_detailed.html", {"request": request})

# TODO: Create a POST endpoint for the post creation form at /feed

# TODO: Create a PUT endpoint for the post edition form at /feed/{post_id}

# TODO: Create a DELETE endpoint for the post deletion form at /feed/{post_id}