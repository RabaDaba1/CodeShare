from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# Import the routes
from routers import login, register

# Create an app object
app = FastAPI()

# Include the routes
app.include_router(login.router)
app.include_router(register.router)

# Mount the templates and static folders
templates = Jinja2Templates(directory="../templates")
app.mount("/static", StaticFiles(directory="../static"), name="static")

# Route for the home page
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})