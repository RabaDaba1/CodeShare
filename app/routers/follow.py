from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db

from crud import crud_user, crud_follow

router = APIRouter()
templates = Jinja2Templates(directory="../templates")


@router.post("/user/{login}/follow", response_class=HTMLResponse, tags=["User"])
async def follow_user(request: Request, login: str, db: Session = Depends(get_db)):
    # Get current user
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/login", status_code=303)
    
    current_user = crud_user.get_current_user(db, token)
    
    # Check if the user exists
    user = crud_user.get_user_by_login(db, login)
    if user is None:
        return templates.TemplateResponse("error.html", {"request": request, "message": f"No permission", "detailed_message": "You can't follow a non-existing user", "current_user": current_user})
    
    # Follow user
    crud_follow.follow_user(db, current_user.user_id, user.user_id)
    
    # Redirect to the previous page
    return RedirectResponse(url=request.headers.get("Referer", "/"), status_code=303)


@router.post("/user/{login}/unfollow", response_class=HTMLResponse, tags=["User"])
async def unfollow_user(request: Request, login: str, db: Session = Depends(get_db)):
     # Get current user
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/login", status_code=303)
    
    current_user = crud_user.get_current_user(db, token)
    
    # Check if the user exists
    user = crud_user.get_user_by_login(db, login)
    if user is None:
        return templates.TemplateResponse("error.html", {"request": request, "message": f"No permission", "detailed_message": "You can't unfollow a non-existing user", "current_user": current_user})

    # Unfollow user
    crud_follow.unfollow_user(db, current_user.user_id, user.user_id)
    
    # Redirect to the previous page
    return RedirectResponse(url=request.headers.get("Referer", "/"), status_code=303)