from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from models import user as models_user
from database import engine

# Import the routes
from routers import login, register, feed, user

# Create an app object
app = FastAPI()

models_user.Base.metadata.create_all(bind=engine)

# Include the routers
app.include_router(login.router)
app.include_router(register.router)
app.include_router(feed.router)
app.include_router(user.router)

# Mount the templates and static folders
templates = Jinja2Templates(directory="../templates")
app.mount("/static", StaticFiles(directory="../static"), name="static")

# Endpoint for the home page
@app.get("/", response_class=HTMLResponse, tags=["Home page"])
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})