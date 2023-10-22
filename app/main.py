from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# Import the routes
from routers import login

app = FastAPI()

app.include_router(login.router)

templates = Jinja2Templates(directory="../templates")

app.mount("/static", StaticFiles(directory="../static"), name="static")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})