from fastapi import APIRouter

router = APIRouter()

@router.get("/user/{username}")
async def get_user(username: str):
    pass