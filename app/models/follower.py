from sqlalchemy import Column, Integer, String, Sequence, Time, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from models.user import User

Base = declarative_base()

class Follower(Base):
    __tablename__ = 'followers'

    follower_id = Column(Integer, ForeignKey(User.user_id), primary_key=True)
    following_id = Column(Integer, ForeignKey(User.user_id), primary_key=True)
    
    