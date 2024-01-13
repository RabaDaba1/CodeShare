from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from crud import create_post, get_current_user, get_user_posts, get_followed, get_user_by_id, get_followers
from database import get_db

router = APIRouter()

templates = Jinja2Templates(directory="../templates")

@router.get("/feed", response_class=HTMLResponse, tags=["Feed"])
async def feed(request: Request, db: Session = Depends(get_db)):
    
    # If user is not logged in, redirect to login page
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/login", status_code=303)

    current_user = get_current_user(db, token)
    followed = get_followed(db, current_user.user_id)

    posts = []

    for user in followed:
        posts.extend(get_user_posts(db, user.following_id))

    posts.extend(get_user_posts(db, current_user.user_id))
    
    posts.sort(key=lambda post: post.date, reverse=True)

    posts_with_authors = [[get_user_by_id(db, post.author_id), post] for post in posts]

    return templates.TemplateResponse("feed.html", {"request": request, "posts": posts_with_authors, "current_user": current_user})

@router.get("/feed/{post_id}", response_class=HTMLResponse, tags=["Feed"])
async def post_detailed(request: Request, post_id: int, db: Session = Depends(get_db)):    
    return templates.TemplateResponse("post_detailed.html", {"request": request})

@router.post("/feed", response_model_exclude_unset=True)
async def new_post(request: Request, description: str = Form(...), programming_language: str = Form(...), code: str = Form(...), output: str = Form(...), db: Session = Depends(get_db)):
    # Get the access token from the cookie
    token = request.cookies.get("access_token")
    
    if not token:
        raise HTTPException(status_code=400, detail="No access token provided")
    
    # Get the current user from the database
    current_user = get_current_user(db, token)
    
    # Create the post
    await create_post(db, current_user.user_id, description, programming_language, code, output)

    # Redirect the user to the feed page
    return RedirectResponse(url="/feed", status_code=303)

# TODO: Create a PUT endpoint for the post edition form at /feed/{post_id}

# TODO: Create a DELETE endpoint for the post deletion form at /feed/{post_id}