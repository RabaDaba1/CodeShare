from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from schemas import PostEdit

# Models
from models.user import User
from models.post import Post

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

async def delete_post(db: Session, post_id: int):
    """
    Deletes a post.
    
    Args:
        post_id (int): ID of the post to be deleted.
        
    Exceptions:
        HTTPException: If the post does not exist.
    """
    post = db.query(Post).filter(Post.post_id == post_id).first()
    
    if post is None:
        raise HTTPException(status_code=400, detail="post does not exists")
    
    db.delete(post)
    
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        print(str(e))  # print the exception details
        raise HTTPException(status_code=400, detail="Can't delete post")

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
    
def edit_post(db: Session, post_id: int, post_edit: PostEdit):
    """
    Edits a post.
    
    Args:
        post_id (int): ID of the post to be edited.
        post_edit (PostEdit): New post data.
        
    Exceptions:
        HTTPException: If the description is too long.
    """
    post = db.query(Post).filter(Post.post_id == post_id).first()
    
    post_data = post_edit.dict(exclude_unset=True)
    for key, value in post_data.items():
        if value:
            setattr(post, key, value)
            
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        print(str(e))  # print the exception details
        raise HTTPException(status_code=400, detail="Can't edit post")