# FastAPI
from fastapi import APIRouter, HTTPException, Request, Depends, status, Form, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

# Database
from schemas import UserCreate
from sqlalchemy.orm import Session
from database import get_db

from crud import crud_user

router = APIRouter()

templates = Jinja2Templates(directory="../templates")

@router.get("/register", response_class=HTMLResponse, tags=["Register"])
async def register_form(request: Request ):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register", response_class=HTMLResponse, tags=["Register"])
def register_user(
    username: str = Form(...),
    login: str = Form(...),
    password: str = Form(...),
    password_repeat: str = Form(...),
    db: Session = Depends(get_db)
):
    # Create a new user
    user = UserCreate(username=username, login=login, password=password, password_repeat=password_repeat)
    
    # Add the user to the database
    user = crud_user.create_user(db, user)
    
    # Check if the user was added successfully
    authenticated_user = crud_user.authenticate_user(user, password)
    
    # If the user was added successfully, generate a token for them and redirect them to the feed page
    # Otherwise, raise an exception
    if authenticated_user:
        access_token = crud_user.create_access_token(data={"sub": user.login})

        response = RedirectResponse(url="/feed", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="access_token", value=access_token, httponly=True)
        return response
    else:
        raise HTTPException(status_code=400, detail="Incorrect username or password")