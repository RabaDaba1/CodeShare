from fastapi import APIRouter, Request, Depends, Form, HTTPException, status
from crud import authenticate_user, create_access_token, get_user_by_login
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter()

templates = Jinja2Templates(directory="../templates")

@router.get("/login", response_class=HTMLResponse, tags=["Login"])
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def login(request: Request, login: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = get_user_by_login(db, login)
    
    if not user or not authenticate_user(user, password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    # If the user is authenticated, generate a token for them
    access_token = create_access_token(data={"sub": user.login})
    
    response = RedirectResponse(url='/feed', status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie("access_token", access_token, httponly=True)
    
    return response

@router.get("/logout")
def logout():
    
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key="access_token")
    
    return response