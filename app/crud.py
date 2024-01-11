from fastapi import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from schemas import UserCreate

# Models
from models.friend_request import FriendRequest
from models.post_like import PostLike
from models.user import User
from models.comment import Comment
from models.friend import Friend
from models.post import Post
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
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        login = payload.get("sub")
        if login is None:
            raise credentials_exception
        user = get_user_by_login(db, login=login)
        if user is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    return user


def get_user_by_login(db: Session, login: str) -> User | None:
    """
    Returns a user with the given login.
    """
    return db.query(User).filter(User.login == login).first()


def follow_user(db: Session, requester_id: int, receiver_id: int) -> FriendRequest:
    """
    Follows a user.
    
    Args:
        requester_id (int): ID of the user sending the request.
        receiver_id (int): ID of the user receiving the request.
        
    Returns:
        FriendRequest: Created friend request object.
        
    Exceptions:
        HTTPException: If the request already exists.
        HTTPException: If the users are already friends.
        HTTPException: If the users are the same.
    """
    
    # TODO: Implement this function
    
def unfollow_user(db: Session, requester_id: int, receiver_id: int) -> FriendRequest:
    """
    Unfollows a user.
    
    Args:
        requester_id (int): ID of the user sending the request.
        receiver_id (int): ID of the user receiving the request.
        
    Returns:
        FriendRequest: Created friend request object.
        
    Exceptions:
        HTTPException: If the request already exists.
        HTTPException: If the users are already friends.
        HTTPException: If the users are the same.
    """
    
    # TODO: Implement this function


def like_post(user_id: int, post_id: int) -> PostLike:
    """
    Adds a like to a post or removes it.
    
    Args:
        user_id (int): ID of the user who liked the post.
        post_id (int): ID of the liked post.
        
    Returns:
        PostLike: Created post like object.
        
    Exceptions:
        HTTPException: If the post does not exist.
    """
    
    # TODO: Implement this function


async def create_post(db: Session, author_id: str, description: str, programming_language, code: str, output: str) -> Post:
    """
    Creates a new post.
    
    Args:
        author_id (int): ID of the post's author.
        description (str): Description of the post.
        date (datetime): Date of post creation.
        programming_language (enum): Programming language used in the code.
        code (str): Source code.
        output (str): Output of the code execution.
        
    Returns:
        Post: Created post object.
        
    Exceptions:
        HTTPException: If the programming language is not supported.
        HTTPException: If the description, code, or output are too long.
    """

    if db.query(User).filter(User.user_id == author_id).first() is None:
        raise HTTPException(status_code=400, detail="user does not exists")

    if description == "":
        raise HTTPException(status_code=400, detail="description cannot be empty")

    new_post = Post(
        author_id=author_id,
        description=description, 
        date=datetime.now(),
        lang=programming_language, 
        code=code, 
        output=output
    )
    
    db.add(new_post)
    
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        print(str(e))  # print the exception details
        raise HTTPException(status_code=400, detail="Can't add post")

    db.refresh(new_post)
    
    return new_post

from sqlalchemy.orm import joinedload

def get_all_posts(db: Session):
    return db.query(Post).all()

def get_user_posts(db: Session, author_login: str):
    author: User
    try:
        author = get_user_by_login(db, author_login)
        return db.query(Post).filter(Post.author_id == author.user_id).all()
    except Exception as e:
        return []
    
def create_comment(author_id: int, post_id: int, content: str, date: datetime) -> Comment:
    """
    Creates a new comment.
    
    Args:
        author_id (int): ID of the comment's author.
        post_id (int): ID of the post to which the comment is added.
        content (str): Content of the comment.
        date (datetime): Date of comment creation.
        
    Returns:
        Comment: Created comment object.
        
    Exceptions:
        HTTPException: If the post does not exist.
        HTTPException: If the content is too long.
    """
    
    # TODO: Implement this function
    
def update_user(db: Session, user_id: int, username: str, login: str, description: str, picture_url: str) -> User:
    """
    Updates user information.
    
    Args:
        user_id (int): ID of the user.
        username (str): New username.
        login (str): New login.
        picture_url (str): New picture URL.
        
    Returns:
        User: Updated user object.
        
    Exceptions:
        HTTPException: If the user does not exist.
        HTTPException: If the login is already taken.
        HTTPException: If the username is too short or too long.
    """