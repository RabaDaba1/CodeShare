from sqlalchemy import Column, Integer, String, Sequence, Time, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, Sequence('post_id_seq'), primary_key=True)
    author_id = Column(Integer, ForeignKey("users.id"))
    description = Column(String(300))
    date = Column(Time)
    lang = Column(Enum("cpp", "java", "python", "csharp"))
    code = Column(String(800), nullable=True)
    output = Column(String(100), nullable=True)