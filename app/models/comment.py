from sqlalchemy import Column, Integer, String, Sequence, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from models.user import User
from models.post import Post

Base = declarative_base()

class Comment(Base):
    __tablename__ = 'comments'
    comment_id = Column(Integer, Sequence('comment_id_seq'), primary_key=True)
    author_id = Column(Integer, ForeignKey(User.user_id))
    post_id = Column(Integer, ForeignKey(Post.post_id))
    content = Column(String(200))
    date = Column(DateTime)