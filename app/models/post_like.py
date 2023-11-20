from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class PostLike(Base):
    __tablename__ = 'post_likes'
    post_id = Column(Integer, ForeignKey("posts.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)