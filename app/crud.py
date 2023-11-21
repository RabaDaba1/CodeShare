from fastapi import HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import datetime

# Models
from models.friend_request import FriendRequest
from models.post_like import PostLike
from models.user import User
from models.comment import Comment
from models.friend import Friend
from models.post import Post
from models.user import User

# Schemas
from schemas.user_schemas import UserCreate

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

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not pwd_context.verify(password, user.hashedPassword):
        return False
    return user

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def send_friend_request(requester_id: int, receiver_id: int) -> FriendRequest:
    """
    Sends a friend request.
    
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

def create_post(db: Session, author_id: int, description: str, date: datetime, lang: enumerate, code: str, output: str) -> Post:
    """
    Creates a new post.
    
    Args:
        author_id (int): ID of the post's author.
        description (str): Description of the post.
        date (datetime): Date of post creation.
        lang (enum): Programming language used in the code.
        code (str): Source code.
        output (str): Output of the code execution.
        
    Returns:
        Post: Created post object.
        
    Exceptions:
        HTTPException: If the programming language is not supported.
        HTTPException: If the description, code, or output are too long.
    """

    if db.query(User).filter(User.id == author_id).first() is None:
        raise HTTPException(status_code=400, detail="user does not exists")

    if description == "":
        raise HTTPException(status_code=400, detail="description cannot be empty")

    new_post = Post(author_id=author_id, description=description, date=date, lang=lang, code=code, output=output)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
    
    # TODO: Implement this function

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