from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from database import get_db
from crud import crud_user, crud_like

router = APIRouter()

templates = Jinja2Templates(directory="../templates")


@router.get("/{post_id}/like")
async def like_post(request: Request, post_id: int, db: Session = Depends(get_db)):  # Zmieniono nazwę funkcji
    # Get the access token from the cookie
    token = request.cookies.get("access_token")
    
    if not token:
        raise HTTPException(status_code=400, detail="No access token provided")
    
    # Get the current user from the database
    current_user = crud_user.get_current_user(db, token)
    
    # Like the post
    await crud_like.like_post(db, current_user.user_id, post_id)  # Wywołanie funkcji like_post z modułu services

    # Redirect the user to the feed page
    return RedirectResponse(url=request.headers.get("Referer", "/"), status_code=303)

@router.get("/{post_id}/unlike")
async def unlike_post(request: Request, post_id: int, db: Session = Depends(get_db)):
    # Get the access token from the cookie
    token = request.cookies.get("access_token")
    
    if not token:
        raise HTTPException(status_code=400, detail="No access token provided")
    
    # Get the current user from the database
    current_user = crud_user.get_current_user(db, token)
    
    # Unlike the post
    await crud_like.unlike_post(db, current_user.user_id, post_id)

    # Redirect the user to the feed page
    return RedirectResponse(url=request.headers.get("Referer", "/"), status_code=303)

