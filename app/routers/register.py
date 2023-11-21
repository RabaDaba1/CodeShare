from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import SessionLocal
from crud import create_user
from models.user import User
from database import get_db

router = APIRouter()

templates = Jinja2Templates(directory="../templates")

@router.get("/register", response_class=HTMLResponse, tags=["Register"])
async def register_form(request: Request ):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/users/")
async def create_user(login: str, username: str, password: str, repeat_password: str, db: Session = Depends(get_db)):
    if password != repeat_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    return create_user(db=db, login=login, username=username, password=password, repeat_password=repeat_password)

# TODO: Create a POST endpoint for the registration form