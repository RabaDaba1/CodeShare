from sqlalchemy import Column, Integer, String, Sequence, Time, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, Sequence('comment_id_seq'), primary_key=True)
    author_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))
    content = Column(String(200))
    date = Column(Time)