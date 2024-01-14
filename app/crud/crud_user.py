from fastapi import HTTPException
from starlette.status import HTTP_307_TEMPORARY_REDIRECT
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from schemas import UserCreate, UserUpdate

# Models
from models.user import User

# Schemas
from schemas import UserCreate

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, user: UserCreate) -> User:
    """
    Creates a new user.
    
    Args:
        login (str): Login of the new user.
        username (str): Name of the new user.
        password (str): Password of the new user.
        
    Returns:
        User: Created user object.
        
    Exceptions:
        HTTPException: If the login is already taken.
        HTTPException: If the passwords don't match.
        HTTPException: If the password is too short or too long.
        HTTPException: If the username is too short or too long.
    """

    if user.password != user.password_repeat:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    hashed_password = pwd_context.hash(user.password)

    db_user = User(username=user.username, login=user.login, hashedPassword=hashed_password, pictureUrl="https://t4.ftcdn.net/jpg/00/64/67/27/360_F_64672736_U5kpdGs9keUll8CRQ3p3YaEv2M6qkVY5.jpg")
    db.add(db_user)
    
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Login already taken")

    db.refresh(db_user)
    
    return db_user

def authenticate_user(user: User, password: str) -> bool:
    """
    Authenticates a user.
    """
    if not pwd_context.verify(password, user.hashedPassword):
        return False
    return True

def create_access_token(*, data: dict, expires_delta: timedelta = None):
    """
    Creates a new access token.
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

def get_current_user(db, token: str) -> User | None:
    if not token:
        raise HTTPException(status_code=400, detail="No access token provided")

    credentials_exception = HTTPException(
        status_code=HTTP_307_TEMPORARY_REDIRECT,
        detail="Invalid credentials",
        headers={"Location": "/login"}
    )
    
    try:        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        login = payload.get("sub")
        if login is None:
            raise credentials_exception
        user = get_user_by_login(db, login)
        if user is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    
    return user

def get_user_by_id(db: Session, user_id: int) -> User | None:
    """
    Returns a user with the given ID.
    """
    return db.query(User).filter(User.user_id == user_id).first()

def get_user_by_login(db: Session, login: str) -> User | None:
    """
    Returns a user with the given login.
    """
    return db.query(User).filter(User.login == login).first()

def update_user(db: Session, user: User, user_update: UserUpdate):
    """
    Updates a user.
    
    Args:
        user (User): User to be updated.
        user_update (UserUpdate): New user data.
    
    Returns:
        User: Updated user object.
        
    Exceptions:
        HTTPException: If the username is too short or too long.
        HTTPException: If the bio is too long.
    """
    user_data = user_update.dict(exclude_unset=True)
    for key, value in user_data.items():
        if not value:
            continue
        
        if key == "password" and value is not None:
            key = "hashedPassword"
            value = pwd_context.hash(value)
            
        setattr(user, key, value)
        
    db.commit()
    db.refresh(user)
      
def get_similar_users(db: Session, username: str):
    return db.query(User).filter(User.username.ilike(f"%{username}%")).all()