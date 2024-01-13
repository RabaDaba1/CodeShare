from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db

from crud import crud_user, crud_post, crud_comment

router = APIRouter()

templates = Jinja2Templates(directory="../templates")


@router.get("/feed/{post_id}", response_class=HTMLResponse, tags=["Feed"])
async def post_detailed(request: Request, post_id: int, db: Session = Depends(get_db)):  
    # Check if user is logged in
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/login", status_code=303)
    
    # Get current user
    current_user = crud_user.get_current_user(db, token)

    post = crud_post.get_post_by_id(db, post_id)
    author = crud_user.get_user_by_id(db, post.author_id)
    comments = crud_comment.get_post_comments(db, post_id)
    comments.sort(key=lambda comment: comment.date, reverse=True)
    comments = [[crud_user.get_user_by_id(db, comment.author_id), comment] for comment in comments]

    return templates.TemplateResponse("post_detailed.html", {"request": request, "post": post, "author": author, "comments": comments, "current_user": current_user})


@router.post("/feed/{post_id}/comment")
async def new_comment(request: Request, post_id: int, content: str = Form(...), db: Session = Depends(get_db)):
    # Check if user is logged in
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=400, detail="No access token provided")
    
    # Get current user
    current_user = crud_user.get_current_user(db, token)
    
    # Create post
    await crud_comment.create_comment(db, current_user.user_id, post_id, content, datetime.now())

    # Redirect the user to the feed page
    return RedirectResponse(url=f"/feed/{post_id}", status_code=303)

@router.get("/post/{post_id}/delete")
async def delete_post(request: Request, post_id: int, db: Session = Depends(get_db)):
    # Check if user is logged in
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=400, detail="No access token provided")
    
    # Get current user
    current_user = crud_user.get_current_user(db, token)
    
    # Delete post
    await crud_post.delete_post(db, post_id)

    # Redirect the user to the feed page
    return RedirectResponse(url="/feed", status_code=303)