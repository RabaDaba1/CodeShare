from sqlalchemy import Column, Integer, Enum, Time, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from models.user import User

Base = declarative_base()

class FriendRequest(Base):
    __tablename__ = 'friend_requests'

    reciver_user_id = Column(Integer, ForeignKey(User.user_id), primary_key=True)
    requester_user_id = Column(Integer, ForeignKey(User.user_id), primary_key=True)
    date = Column(Time)
    status = Column(Enum("accepted", "pending", "rejected"))
    
    