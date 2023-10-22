from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

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
@app.get("/", response_class=HTMLResponse, tags=["Home page"])
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})