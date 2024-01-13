from fastapi import APIRouter, Request, Depends, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db

from crud import crud_like, crud_post, crud_user

router = APIRouter()

templates = Jinja2Templates(directory="../templates")

@router.get("/login", response_class=HTMLResponse, tags=["Login"])
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def login(request: Request, login: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = crud_user.get_user_by_login(db, login)
    
    # If the user is not authenticated, raise an exception
    if not user or not crud_user.authenticate_user(user, password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    # If the user is authenticated, generate a token for them
    access_token = crud_user.create_access_token(data={"sub": user.login})
    
    # Redirect the user to the feed page and set the access token as a cookie
    response = RedirectResponse(url='/feed', status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie("access_token", access_token, httponly=True)
    
    # Return the response
    return response

@router.get("/logout")
async def logout():
    # Redirect the user to the main page and delete the access token cookie
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key="access_token")
    
    return response