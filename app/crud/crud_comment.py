from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

# Models
from models.comment import Comment
from models.post import Post

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
  