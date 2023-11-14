from fastapi import HTTPException
import datetime

def create_user(login: str, username: str, password: str) -> User:
    """
    Creates a new user.
    
    Args:
        login (str): Login of the new user.
        username (str): Name of the new user.
        password (str): Password of the new user.
        
    Returns:
        User: Created user object.
    """

def send_friend_request(requester_id: int, receiver_id: int) -> FriendRequest:
    """
    Sends a friend request.
    
    Args:
        requester_id (int): ID of the user sending the request.
        receiver_id (int): ID of the user receiving the request.
        
    Returns:
        FriendRequest: Created friend request object.
    """

def like_post(user_id: int, post_id: int) -> PostLike:
    """
    Adds a like to a post.
    
    Args:
        user_id (int): ID of the user who liked the post.
        post_id (int): ID of the liked post.
        
    Returns:
        PostLike: Created post like object.
    """

def create_post(author_id: int, description: str, date: datetime, lang: enum, code: str, output: str) -> Post:
    """
    Creates a new post.
    
    Args:
        author_id (int): ID of the post's author.
        description (str): Description of the post.
        date (datetime): Date of post creation.
        lang (enum): Programming language used in the code.
        code (str): Source code.
        output (str): Output of the code execution.
        
    Returns:
        Post: Created post object.
    """

def create_comment(author_id: int, post_id: int, content: str, date: datetime) -> Comment:
    """
    Creates a new comment.
    
    Args:
        author_id (int): ID of the comment's author.
        post_id (int): ID of the post to which the comment is added.
        content (str): Content of the comment.
        date (datetime): Date of comment creation.
        
    Returns:
        Comment: Created comment object.
    """