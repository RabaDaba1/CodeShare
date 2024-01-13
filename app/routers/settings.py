from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from schemas import UserUpdate
from database import get_db
from crud import crud_user

router = APIRouter()
templates = Jinja2Templates(directory="../templates")


@router.get("/settings", response_class=HTMLResponse, tags=["Settings"])
async def user_settings(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/login", status_code=303)
    
    current_user = crud_user.get_current_user(db, token)
    
    return templates.TemplateResponse("user_settings.html", {"request": request, "current_user": current_user})


@router.post("/settings", response_class=HTMLResponse, tags=["Settings"])
async def update_user(request: Request, username: str = Form(None), bio: str = Form(None), pic: str = Form(None), password: str = Form(None), db: Session = Depends(get_db)):
    # Get the user from the database
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/login", status_code=303)
    
    current_user = crud_user.get_current_user(db, token)
    
    # Check if the user is the same as the current user
    if current_user.user_id != current_user.user_id:
        return templates.TemplateResponse("error.html", {"request": request, "message": f"No permission", "detailed_message": "You can't update other user's settings", "current_user": current_user})
    
    # Check if the user exists
    if current_user is None:
        return templates.TemplateResponse("error.html", {"request": request, "message": f"No permission", "detailed_message": "You can't update a non-existing user", "current_user": current_user})
    
    # Update user
    user_update = UserUpdate(username=username, bio=bio, pictureUrl=pic, password=password)
    
    crud_user.update_user(db, current_user, user_update)
    
    return templates.TemplateResponse("user_settings.html", {"request": request, "current_user": current_user})