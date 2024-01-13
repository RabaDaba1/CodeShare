from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from database import get_db
from crud import crud_user, crud_post, crud_follow

router = APIRouter()

templates = Jinja2Templates(directory="../templates")


@router.get("/feed", response_class=HTMLResponse, tags=["Feed"])
async def feed(request: Request, db: Session = Depends(get_db)):
    # Check if user is logged in
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/login", status_code=303)

    # Get current user
    current_user = crud_user.get_current_user(db, token)
    
    followed = crud_follow.get_followed(db, current_user.user_id)

    posts = []

    for user in followed:
        posts.extend(crud_post.get_user_posts(db, user.following_id))

    posts.extend(crud_post.get_user_posts(db, current_user.user_id))
    
    posts.sort(key=lambda post: post.date, reverse=True)

    posts_with_authors = [[crud_user.get_user_by_id(db, post.author_id), post] for post in posts]

    return templates.TemplateResponse("feed.html", {"request": request, "posts": posts_with_authors, "current_user": current_user})


@router.post("/feed", response_model_exclude_unset=True)
async def new_post(request: Request, description: str = Form(...), programming_language: str = Form(...), code: str = Form(...), output: str = Form(None), db: Session = Depends(get_db)):
    # Check if user is logged in
    token = request.cookies.get("access_token")
    
    if not token:
        raise HTTPException(status_code=400, detail="No access token provided")
    
    # Get current user
    current_user = crud_user.get_current_user(db, token)
    
    # Create the post
    code = '\n'.join([line.lstrip() for line in code.split('\n')])
    await crud_post.create_post(db, current_user.user_id, description, programming_language, code, output)

    # Redirect the user to the feed page
    return RedirectResponse(url="/feed", status_code=303)


# TODO: Create a PUT endpoint for the post edition form at /feed/{post_id}

# TODO: Create a DELETE endpoint for the post deletion form at /feed/{post_id}