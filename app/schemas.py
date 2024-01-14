from fastapi import Form
from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str = Form(...)
    login: str = Form(...)
    password: str = Form(...)
    password_repeat: str = Form(...)
    
    
class UserUpdate(BaseModel):
    username: Optional[str] = None
    bio: Optional[str] = None
    pictureUrl: Optional[str] = None
    password: Optional[str] = None
    
class PostEdit(BaseModel):
    description: Optional[str] = None
    code: Optional[str] = None
    output: Optional[str] = None