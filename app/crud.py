from fastapi import HTTPException
from models.user import User
from models.post_like import PostLike
from models.comment import Comment
from models.post import Post
import datetime

def create_user(login: str, username: str, password: str) -> User:
    pass

def send_friend_request(requester_id: int, receiver_id: int) -> FriendRequest:
    pass

def like_post(user_id: int, post_id: int) -> PostLike:
    pass

def create_post(author_id: int, description: str, date: datetime, lang: enum, code: str, output: str) -> Post:
    pass

def create_comment(author_id: int, post_id: int, content: str, date: datetime) -> Comment:
    pass
