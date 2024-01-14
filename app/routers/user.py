from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db

from crud import crud_user, crud_post, crud_follow, crud_like

router = APIRouter()
templates = Jinja2Templates(directory="../templates")


@router.get("/user/{login}", response_class=HTMLResponse, tags=["User"])
async def user_page(request: Request, login: str, db: Session = Depends(get_db)):
    # Not logged in users can't see user pages
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/login", status_code=303)

    # Check if the user exists
    user = crud_user.get_user_by_login(db, login)
    if user is None:
        return templates.TemplateResponse("error.html", {"request": request, "message": f"User {login} not found", "detailed_message": "Sorry, we couldn't find the user you were looking for.", "current_user": crud_user.get_current_user(db, token)})
    
    # Get the current user
    current_user = crud_user.get_current_user(db, token)

    # Get the user's posts
    posts = [[user, post, crud_like.is_liked(db, current_user.user_id, post.post_id)] for post in crud_post.get_user_posts(db, user.user_id)]
    posts.sort(key=lambda post: post[1].date, reverse=True)
    
    # Check if the current user is following the user
    follows = crud_follow.is_following(db, current_user.user_id, user.user_id)

    # Get the user's followers and followed users
    followers = crud_follow.get_followers(db, user.user_id)
    followed = crud_follow.get_followed(db, user.user_id)

    followers = [crud_user.get_user_by_id(db, user.follower_id) for user in followers]
    followed = [crud_user.get_user_by_id(db, user.following_id) for user in followed]
    
    # Get the users followed by the current user
    users_followed_by_current_user = [crud_user.get_user_by_id(db, user.following_id) for user in crud_follow.get_followed(db, current_user.user_id)]

    return templates.TemplateResponse("user.html", {"request": request, "posts": posts, "user": user, "current_user": current_user, 
                                                    "follows": follows, "followers": followers, "followed": followed, "users_followed_by_current_user": users_followed_by_current_user})

# TODO: Create a DELETE endpoint for deleting user account at /user/{username}