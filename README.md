# Code Share
A social media platform for software developers and sharing interesting code snippets.

**Technology stack**:
- **FastAPI** is used to build the main application and define all the API .
- **Uvicorn** serves the FastAPI application.
- **Jinja2** renders HTML templates for the frontend.
- **SQLAlchemy** connects with a database.

## Libraries

### Instalation
``` bash
pip install fastapi uvicorn Jinja2 SQLAlchemy
```

### Run the app
``` bash
cd src
uvicorn main:app --reload
```
Then go to the `http://localhost:8000/`


## Project structure

### Directories
Each of those folders contain:
- `requirements` files that lists all the Python dependencies needed.
- `src` main source directory of this project. It contains the core logic of your application.
- `models` SQLAlchemy models.
- `routers` FastAPI routers.
- `templates` all the HTML templates.

### Files
- `.env` stores environment variables.
- `.gitignore` file to ignore files and directories.
- `README.md` project documentation.
- `main.py` entry point of the application where is an instance of the FastAPI class and the routers.
