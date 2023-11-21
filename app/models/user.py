from fastapi import HTTPException
from sqlalchemy import Column, Integer, Null, String, Sequence
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    login = Column(String(16))
    username = Column(String(32))
    password = Column(String(32))
    bio = Column(String(300), nullable=True)
    pictureUrl = Column(String(200), nullable=True)
    
    def compare_passwords(str1, str2):
        errors = []
        if len(str1) > 32 or len(str1 < 6):
            errors.append("The password should be between 6 and 32 characters long")

        if not (any(char.isdigit() for char in str1) and any(char.isalpha() for char in str1)):
            errors.append("Password should contain both letters and numbers.")

        if str1 != str2:
            errors.append("The given passwords do not match.")

        if errors:
            raise HTTPException("\n".join(errors))
        
    def __init__(self, log, un, pas, rep_pass):
        try:
           if len(un) > 32 or len(un < 6):
            raise HTTPException("The username should be between 6 and 32 characters long")
           self.compare_passwords(pas, rep_pass) 
           self.login = log
           self.username = un
           self.password = pas
           self.bio = Null
           self.pictureUrl = Null
         
        except HTTPException as e:
            print(e)
            
        
    