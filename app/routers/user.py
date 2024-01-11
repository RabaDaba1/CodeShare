from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from crud import get_user_posts, get_current_user, get_user_by_login
from database import get_db
from sqlalchemy.orm import Session
from models.user import User

router = APIRouter()
templates = Jinja2Templates(directory="../templates")

@router.get("/user/{login}", response_class=HTMLResponse, tags=["User"])
async def user_page(request: Request, login: str, db: Session = Depends(get_db)):
    user = get_user_by_login(db, login)
    if user is None:
        return templates.TemplateResponse("error.html", {"request": request, "message": f"User {login} not found", "detailed_message": "Sorry, we couldn't find the user you were looking for."})
    
    posts = get_user_posts(db, login)
    
    current_user = get_current_user(db, request.cookies.get("access_token"))

    return templates.TemplateResponse("user.html", {"request": request, "login": login, "posts": posts, "user": current_user})


@router.get("/user/{login}/settings", response_class=HTMLResponse, tags=["User"])
async def user_settings(request: Request, login: str, db: Session = Depends(get_db)):
    user = get_user_by_login(db, login)
    if user is None:
        return templates.TemplateResponse("error.html", {"request": request, "message": f"No permission", "detailed_message": "You can't access other user's settings"})
    
    return templates.TemplateResponse("user_settings.html", {"request": request, "login": login})

# TODO: Create a PUT endpoint for updating user information at /user/{username}

# TODO: Create a DELETE endpoint for deleting user account at /user/{username}

# TODO: Create a POST endpoint for starting to follow a user at /user/{username}/follow

# TODO: Create a DELETE endpoint for stopping to follow a user at /user/{username}/follow