from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from schemas import UserUpdate
from models.user import User
from database import get_db
from crud import get_user_posts, get_current_user, get_user_by_login, is_following, get_followers, get_followed, get_user_by_id
import crud


router = APIRouter()
templates = Jinja2Templates(directory="../templates")

@router.get("/user/{login}", response_class=HTMLResponse, tags=["User"])
async def user_page(request: Request, login: str, db: Session = Depends(get_db)):
    # Not logged in users can't see user pages
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/login", status_code=303)

    # Check if the user exists
    user = get_user_by_login(db, login)
    if user is None:
        return templates.TemplateResponse("error.html", {"request": request, "message": f"User {login} not found", "detailed_message": "Sorry, we couldn't find the user you were looking for.", "current_user": get_current_user(db, token)})
    
    # Get the user's posts
    posts = [[user, post] for post in get_user_posts(db, user.user_id)]
    posts.sort(key=lambda post: post[1].date, reverse=True)
    
    # Get the current user
    current_user = get_current_user(db, token)
    
    # Check if the current user is following the user
    follows = is_following(db, current_user.user_id, user.user_id)

    # Get the user's followers and followed users
    followers = get_followers(db, user.user_id)
    followed = get_followed(db, user.user_id)

    followers = [get_user_by_id(db, user.follower_id) for user in followers]
    followed = [get_user_by_id(db, user.following_id) for user in followed]
    
    # Get the users followed by the current user
    users_followed_by_current_user = [get_user_by_id(db, user.following_id) for user in get_followed(db, current_user.user_id)]

    return templates.TemplateResponse("user.html", {"request": request, "posts": posts, "user": user, "current_user": current_user, 
                                                    "follows": follows, "followers": followers, "followed": followed, "users_followed_by_current_user": users_followed_by_current_user})


@router.post("/user/{login}/follow", response_class=HTMLResponse, tags=["User"])
async def follow_user(request: Request, login: str, db: Session = Depends(get_db)):
    # Check if the user exists
    user = get_user_by_login(db, login)
    if user is None:
        return templates.TemplateResponse("error.html", {"request": request, "message": f"No permission", "detailed_message": "You can't follow a non-existing user"})
    
    # Get the current user from the database
    current_user = get_current_user(db, request.cookies.get("access_token"))
    
    # Follow user
    crud.follow_user(db, current_user.user_id, user.user_id)
    
    # Redirect to the previous page
    return RedirectResponse(url=request.headers.get("Referer", "/"), status_code=303)


@router.post("/user/{login}/unfollow", response_class=HTMLResponse, tags=["User"])
async def unfollow_user(request: Request, login: str, db: Session = Depends(get_db)):
    # Check if the user exists
    user = get_user_by_login(db, login)
    if user is None:
        return templates.TemplateResponse("error.html", {"request": request, "message": f"No permission", "detailed_message": "You can't unfollow a non-existing user"})
    
    # Get the current user from the database
    current_user = get_current_user(db, request.cookies.get("access_token"))
    
    # Unfollow user
    crud.unfollow_user(db, current_user.user_id, user.user_id)
    
    # Redirect to the previous page
    return RedirectResponse(url=request.headers.get("Referer", "/"), status_code=303)


@router.get("/settings", response_class=HTMLResponse, tags=["Settings"])
async def user_settings(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/login", status_code=303)
    
    user = get_current_user(db, token)
    
    return templates.TemplateResponse("user_settings.html", {"request": request, "current_user": user})


@router.post("/settings", response_class=HTMLResponse, tags=["Settings"])
async def update_user(request: Request, username: str = Form(None), bio: str = Form(None), pic: str = Form(None), password: str = Form(None), db: Session = Depends(get_db)):
    # Get the user from the database
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/login", status_code=303)
    
    user = get_current_user(db, token)
    current_user = get_current_user(db, request.cookies.get("access_token"))
    
    # Check if the user is the same as the current user
    if user.user_id != current_user.user_id:
        return templates.TemplateResponse("error.html", {"request": request, "message": f"No permission", "detailed_message": "You can't update other user's settings"})
    
    # Check if the user exists
    if user is None:
        return templates.TemplateResponse("error.html", {"request": request, "message": f"No permission", "detailed_message": "You can't update a non-existing user"})
    
    # Update user
    user_update = UserUpdate(username=username, bio=bio, pictureUrl=pic, password=password)
    
    crud.update_user(db, user, user_update)
    
    return templates.TemplateResponse("user_settings.html", {"request": request, "current_user": user})

# TODO: Create a DELETE endpoint for deleting user account at /user/{username}