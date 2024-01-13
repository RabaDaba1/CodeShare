from fastapi import HTTPException
from starlette.status import HTTP_307_TEMPORARY_REDIRECT
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from schemas import UserCreate

# Models
from models.post_like import PostLike
from models.user import User
from models.comment import Comment
from models.follower import Follower
from models.post import Post
from models.user import User

from sqlalchemy.exc import IntegrityError

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
        user = get_user_by_login(db, login=login)
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

def follow_user(db: Session, follower_id: int, following_id: int) -> Follower:
    """
    Follows a user.
    
    Args:
        follower_id (int): ID of the user who wants to follow.
        following_id (int): ID of the user to be followed.
        
    Returns:
        Follower: Created follower object.
        
    Exceptions:
        HTTPException: If the follower_id and following_id are the same.
        HTTPException: If the follower is already following the user.
    """

    if follower_id == following_id:
        raise HTTPException(status_code=400, detail="Users are the same")

    follower = Follower(follower_id=follower_id, following_id=following_id)

    db.add(follower)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="User is already following")

    db.refresh(follower)

    return follower
    
def unfollow_user(db: Session, follower_id: int, following_id: int):
    """
    Unfollows a user.
    
    Args:
        follower_id (int): ID of the user who wants to unfollow.
        following_id (int): ID of the user to be unfollowed.
        
    Returns:
        dict: A message indicating the operation was successful.
        
    Exceptions:
        HTTPException: If the follower_id and following_id are the same.
        HTTPException: If the follower is not following the user.
    """

    if follower_id == following_id:
        raise HTTPException(status_code=400, detail="Users are the same")

    follower = db.query(Follower).filter(Follower.follower_id == follower_id, Follower.following_id == following_id).first()

    if not follower:
        raise HTTPException(status_code=400, detail="User is not following")

    db.delete(follower)
    db.commit()

    return {"detail": "Unfollowed successfully"}
    
def is_following(db: Session, follower_id: int, following_id: int) -> bool:
    """
    Checks if a user is following another user.
    
    Args:
        follower_id (int): ID of the user who might be following.
        following_id (int): ID of the user who might be followed.
        
    Returns:
        bool: True if the user is following the other user, False otherwise.
    """
    
    follower = db.query(Follower).filter(Follower.follower_id == follower_id, Follower.following_id == following_id).first()

    return follower is not None

def get_followed(db: Session, user_id: int):
    """
    Returns a list of users that the user follows.
    
    Args:
        user_id (int): ID of the user.
        
    Returns:
        List[User]: List of users that the user follows.
    """
    
    followed = db.query(Follower).filter(Follower.follower_id == user_id).all()

    return followed

def get_followers(db: Session, user_id: int):
    """
    Returns a list of users that follow the user.
    
    Args:
        user_id (int): ID of the user.
        
    Returns:
        List[User]: List of users that follow the user.
    """
    
    followers = db.query(Follower).filter(Follower.following_id == user_id).all()

    return followers

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

def get_all_posts(db: Session):
    return db.query(Post).all()

def get_post_by_id(db:Session, post_id: int):
    return db.query(Post).filter(Post.post_id == post_id).first()

def get_user_posts(db: Session, user_id: str):
    author: User
    try:
        author = db.query(User).filter(User.user_id == user_id).first()
        return db.query(Post).filter(Post.author_id == author.user_id).all()
    except Exception as e:
        return []
    
async def create_comment(db: Session, author_id: int, post_id: int, content: str, date: datetime) -> Comment:
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
    
    if db.query(Post).filter(Post.post_id == post_id).first() is None:
        raise HTTPException(status_code=400, detail="Post does not exist")
    if len(content) > 200:
        raise HTTPException(status_code=400, detail="Content is too long")
    new_comment = Comment(
        author_id=author_id,
        post_id=post_id,
        content=content,
        date=date
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

def get_post_comments(db: Session, post_id: int):
    """
    Returns a list of comments of a post.
    
    Args:
        post_id (int): ID of the post.
        
    Returns:
        List[Comment]: List of comments of the post.
    """
    
    return db.query(Comment).filter(Comment.post_id == post_id).all()

def get_comment_by_id(db: Session, comment_id: int):
    """
    Returns a comment with the given ID.
    
    Args:
        comment_id (int): ID of the comment.
        
    Returns:
        Comment: Comment with the given ID.
    """
    
    return db.query(Comment).filter(Comment.comment_id == comment_id).first()
  
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
    
def get_similar_users(db: Session, username: str):
    return db.query(User).filter(User.username.ilike(f"%{username}%")).all()