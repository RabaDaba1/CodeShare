from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from models import user as models_user
from models import comment as models_comment
from models import follower as models_follower
from models import post_like as models_post_like
from models import post as models_post
from database import get_db
from database import engine
from crud import crud_user

# Import the routes
from routers import feed, follow, like, login, post, register, search, settings, user

# Create an app object
app = FastAPI()

models_user.Base.metadata.create_all(bind=engine)
models_comment.Base.metadata.create_all(bind=engine)
models_follower.Base.metadata.create_all(bind=engine)
models_post.Base.metadata.create_all(bind=engine)
models_post_like.Base.metadata.create_all(bind=engine)

# Include the routers
app.include_router(feed.router)
app.include_router(follow.router)
app.include_router(like.router)
app.include_router(login.router)
app.include_router(post.router)
app.include_router(register.router)
app.include_router(search.router)
app.include_router(settings.router)
app.include_router(user.router)
    
# Mount the templates and static folders
templates = Jinja2Templates(directory="../templates")
app.mount("/static", StaticFiles(directory="../static"), name="static")

# Endpoint for the home page
@app.get("/", response_class=HTMLResponse, tags=["Home page"])
async def home(request: Request, db = Depends(get_db)):
    # Get current user
    token = request.cookies.get("access_token")
    current_user = None
    if token:
        current_user = crud_user.get_current_user(db, token)
    
    return templates.TemplateResponse("index.html", {"request": request, "current_user": current_user})