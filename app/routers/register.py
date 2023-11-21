# FastAPI
from fastapi import APIRouter, HTTPException, Request, Depends, status, Form, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

# Database
from schemas import UserCreate
from sqlalchemy.orm import Session
from crud import create_user, authenticate_user, create_access_token
from database import get_db

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
    user = UserCreate(username=username, login=login, password=password, password_repeat=password_repeat)
    
    user = create_user(db, user)
    
    authenticated_user = authenticate_user(user, password)
    
    if authenticated_user:
        access_token = create_access_token(data={"sub": user.login})

        response = RedirectResponse(url="/feed", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="access_token", value=access_token, httponly=True)
        return response
    else:
        raise HTTPException(status_code=400, detail="Incorrect username or password")