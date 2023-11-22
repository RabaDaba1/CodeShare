from fastapi import APIRouter, Path, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from http.client import HTTPException
from fastapi import APIRouter, Depends, Request, Session
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from database import get_db
from models.user import User 
from http.client import HTTPException
from models.user import User 
from crud import authenticate_user

router = APIRouter()
templates = Jinja2Templates(directory="../templates")




@router.get("/user/{login}/settings", response_class=HTMLResponse, tags=["User"])
async def user_page(request: Request, login: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.login == login).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with the login {login} is not available")
    return templates.TemplateResponse("user.html", {"request": request, "login": user.login})


@router.put("/user/:")
def update_user(
    username: str = None,
    login: str = Path(..., title="The username of the user to update"),
    new_username: str = None,
    password: str = None,
    current_password: str = None,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.login == login).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User {login} not found")
    
    if not authenticate_user(login, password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    
    if login:
        user.login = login
    if new_username:
        user.username = new_username
    if password:
        user.password = password  

    db.commit()
    return {"message": "User information updated successfully"}


@router.delete("/user/:login")
def delete_user(password: str, login: str = Path(..., title="The login of the user to delete"), db: Session = Depends(get_db)):
    if not authenticate_user(login, password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    user = db.query(User).filter(User.login == login).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with username {login} not found")
    db.delete(user)
    db.commit()
    return {"message": f"User {login} has been deleted"}

# TODO: Create a POST endpoint for starting to follow a user at /user/{username}/follow

# TODO: Create a DELETE endpoint for stopping to follow a user at /user/{username}/follow
