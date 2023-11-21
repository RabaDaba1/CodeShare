from fastapi import HTTPException
from sqlalchemy import Column, Integer, Null, String, Sequence
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    login = Column(String(16), unique=True)
    username = Column(String(32))
    password = Column(String(32))
    bio = Column(String(300), nullable=True)
    pictureUrl = Column(String(200), nullable=True)

            
        
    