from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db
from crud import create_user
router = APIRouter()

templates = Jinja2Templates(directory="../templates")

@router.get("/register", response_class=HTMLResponse, tags=["Register"])
async def register_form(request: Request ):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register")
def create_user_endpoint(login: str, username: str, password: str, repeat_password: str, db: Session = Depends(next(get_db()))):
    if password != repeat_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    
    return create_user(db=db, login=login, username=username, password=password, repeat_password=repeat_password)