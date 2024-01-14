from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

# Models
from models.post_like import PostLike

async def like_post(db: Session, user_id: int, post_id: int) -> PostLike:
    """
    Likes a post.
    
    Args:
        user_id (int): ID of the user who wants to like the post.
        post_id (int): ID of the post to be liked.
        
    Returns:
        PostLike: Created post like object.
        
    Exceptions:
        HTTPException: If the user already liked the post.
    """

    post_like = PostLike(user_id=user_id, post_id=post_id)

    db.add(post_like)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="User already liked the post")

    db.refresh(post_like)

    return post_like

async def unlike_post(db: Session, user_id: int, post_id: int):
    """
    Unlikes a post.
    
    Args:
        user_id (int): ID of the user who wants to unlike the post.
        post_id (int): ID of the post to be unliked.
        
    Returns:
        dict: A message indicating the operation was successful.
        
    Exceptions:
        HTTPException: If the user did not like the post.
    """

    post_like = db.query(PostLike).filter(PostLike.user_id == user_id, PostLike.post_id == post_id).first()

    if not post_like:
        raise HTTPException(status_code=400, detail="User did not like the post")

    db.delete(post_like)
    
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="User already disliked the post")

    return {"detail": "Unliked successfully"}

def is_liked (db: Session, user_id: int, post_id: int) -> bool:
    """
    Checks if a post is liked by a user.
    
    Args:
        user_id (int): ID of the user.
        post_id (int): ID of the post.
        
    Returns:
        bool: True if the post is liked by the user, False otherwise.
    """

    post_like = db.query(PostLike).filter(PostLike.user_id == user_id, PostLike.post_id == post_id).first()

    return post_like is not None