from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud import get_similar_users
from database import get_db

router = APIRouter()

@router.get("/search/")
def read_users(username: str = '', db: Session = Depends(get_db)):    
    users = get_similar_users(db, username=username)
    
    if users is None:
        raise HTTPException(status_code=404, detail="Users not found")
    
    return users