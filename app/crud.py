
from models.user import User
from models.post_like import PostLike
from models.comment import Comment
from models.post import Post
from models.friend import Friend
from models.friend_request import FriendRequest
from sqlalchemy.orm import Session
import datetime
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash
from models.user import User
from fastapi import HTTPException


def create_user(db: Session, login: str, username: str, password: str, repeat_password: str) -> User:
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

    if password != repeat_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    hashed_password = generate_password_hash(password)

    db_user = User(username=username, login=login, password=hashed_password)
    db.add(db_user)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Login already taken")

    db.refresh(db_user)
    return db_user
    
    # TODO: Implement this function

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