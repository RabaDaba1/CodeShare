from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from models.user import User
from crud import get_user_by_login, create_post, get_current_user
from database import get_db

router = APIRouter()

templates = Jinja2Templates(directory="../templates")

@router.get("/feed", response_class=HTMLResponse, tags=["Feed"])
async def feed(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("feed.html", {"request": request})

@router.get("/feed/{post_id}", response_class=HTMLResponse, tags=["Feed"])
async def post_detailed(request: Request, post_id: int):
    # TODO: Get the post from the database and pass it to the template
    return templates.TemplateResponse("post_detailed.html", {"request": request})

@router.post("/feed", response_model_exclude_unset=True)
async def create_post(request: Request, description: str = Form(...), programming_language: str = Form(...), code: str = Form(...), output: str = Form(...), db: Session = Depends(get_db)):
    #  Get the access token from the cookie
    token = request.cookies.get("access_token")
    
    if not token:
        raise HTTPException(status_code=400, detail="No access token provided")
    
    # Get the current user from the database
    current_user = get_current_user(db, token)
    
    print(current_user.id, current_user.login)
    
    # Create the post
    create_post(db, current_user.id, description, programming_language, code, output)
    
    # Redirect the user to the feed page
    return RedirectResponse(url="/feed", status_code=303)

# TODO: Create a PUT endpoint for the post edition form at /feed/{post_id}

# TODO: Create a DELETE endpoint for the post deletion form at /feed/{post_id}