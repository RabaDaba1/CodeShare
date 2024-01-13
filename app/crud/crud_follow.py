from fastapi import HTTPException
from sqlalchemy.orm import Session

# Models
from models.follower import Follower

from sqlalchemy.exc import IntegrityError

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