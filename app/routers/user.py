from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="../templates")

@router.get("/user/{login}", response_class=HTMLResponse, tags=["User"])
async def get_user(request: Request, login: str):
    # TODO
    # 1) Get user data from the database
    # 2) Send the data to the template
    return templates.TemplateResponse("user.html", {"request": request, "login": login})


@router.get("/user/{login}/settings", response_class=HTMLResponse, tags=["User Settings"])
async def user_settings(request: Request, login: str):
    return templates.TemplateResponse("user_settings.html", {"request": request, "login": login})

# TODO: Create a PUT endpoint for updating user information at /user/{username}

# TODO: Create a DELETE endpoint for deleting user account at /user/{username}

# TODO: Create a POST endpoint for starting to follow a user at /user/{username}/follow

# TODO: Create a DELETE endpoint for stopping to follow a user at /user/{username}/follow

# TODO: Create a GET endpoint for displaying a list of users following a user at /user/{username}/followers

# TODO: Create a GET endpoint for displaying a list of users a user is following at /user/{username}/following