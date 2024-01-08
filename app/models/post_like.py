from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from models.user import User
from models.post import Post

Base = declarative_base()

class PostLike(Base):
    __tablename__ = 'post_likes'
    post_id = Column(Integer, ForeignKey(Post.post_id), primary_key=True)
    user_id = Column(Integer, ForeignKey(User.user_id), primary_key=True)