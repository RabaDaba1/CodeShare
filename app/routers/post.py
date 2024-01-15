from fastapi import APIRouter, Request, Depends, Form, Body
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from schemas import PostEdit
from database import get_db

from crud import crud_user, crud_post, crud_comment, crud_like

router = APIRouter()

templates = Jinja2Templates(directory="../templates")


@router.get("/post/{post_id}", response_class=HTMLResponse, tags=["Feed"])
async def post_detailed(request: Request, post_id: int, db: Session = Depends(get_db)):  
    # Check if user is logged in
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/login", status_code=303)
    
    # Get current user
    current_user = crud_user.get_current_user(db, token)

    post = crud_post.get_post_by_id(db, post_id)
    
    if not post:
        return templates.TemplateResponse("error.html", {"request": request, "message": "Post not found.", "detailed_message": "The post you are looking for does not exist.", "current_user": current_user})
    
    author = crud_user.get_user_by_id(db, post.author_id)
    
    comments = crud_comment.get_post_comments(db, post_id)
    comments.sort(key=lambda comment: comment.date, reverse=True)
    comments = [[crud_user.get_user_by_id(db, comment.author_id), comment] for comment in comments]
    
    is_liked = crud_like.is_liked(db, current_user.user_id, post_id)
    like_count = crud_like.get_like_count(db, post_id)
    
    return templates.TemplateResponse("post_detailed.html", {"request": request, "post": post, "author": author, 
                                                             "comments": comments, "current_user": current_user, 
                                                             "is_liked": is_liked, "like_count": like_count})


@router.post("/post/{post_id}/comment")
async def new_comment(request: Request, post_id: int, content: str = Form(...), db: Session = Depends(get_db)):
    # Check if user is logged in
    token = request.cookies.get("access_token")
    if not token:
        raise RedirectResponse(url="/login", status_code=303)
    
    # Get current user
    current_user = crud_user.get_current_user(db, token)
    
    # Create post
    await crud_comment.create_comment(db, current_user.user_id, post_id, content, datetime.now())

    # Redirect the user to the feed page
    return RedirectResponse(url=f"/post/{post_id}", status_code=303)


@router.get("/post/{post_id}/delete")
async def delete_post(request: Request, post_id: int, db: Session = Depends(get_db)):
    # Check if user is logged in
    token = request.cookies.get("access_token")
    if not token:
        raise RedirectResponse(url="/login", status_code=303)
    
    # Get current user
    current_user = crud_user.get_current_user(db, token)
    post = crud_post.get_post_by_id(db, post_id)
    
    # Check if user is the author of the post
    if current_user.user_id != post.author_id:
        raise HTTPException(status_code=400, detail="You can't delete not your post.")
    
    # Delete post
    await crud_post.delete_post(db, post_id)

    # Redirect the user to the previous page
    return RedirectResponse(url='/feed', status_code=303)


@router.post("/post/{post_id}/edit", response_class=HTMLResponse, tags=["Feed"])
async def edit_post(request: Request, post_id: int, post_edit: PostEdit = Body(...), db: Session = Depends(get_db)):
    # Check if user is logged in
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/login", status_code=303)
    
    # Get current user
    current_user = crud_user.get_current_user(db, token)
    
    post_author = crud_post.get_post_by_id(db, post_id).author_id
    
    if current_user.user_id != post_author:
        raise HTTPException(status_code=400, detail="You can't edit not your post.")
    
    # Edit post
    crud_post.edit_post(db, post_id, post_edit)

    # Redirect the user to previous page
    return RedirectResponse(url=request.headers["Referer"], status_code=303)