from sqlalchemy import Column, Integer, String, Sequence, Time, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from models.user import User

Base = declarative_base()

class Friend(Base):
    __tablename__ = 'friends'

    user_id = Column(Integer, ForeignKey(User.user_id), primary_key=True)
    friend_id = Column(Integer, ForeignKey(User.user_id), primary_key=True)
    
    