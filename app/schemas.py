from fastapi import Form
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str = Form(...)
    login: str = Form(...)
    password: str = Form(...)
    password_repeat: str = Form(...)