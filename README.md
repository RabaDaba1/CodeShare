# CodeShare
A social media platform for software developers and sharing interesting code snippets.

**Technology stack**:
- **FastAPI** is used to build the main application and define all the API .
- **Uvicorn** serves the FastAPI application.
- **Jinja2** renders HTML templates for the frontend.
- **SQLAlchemy** connects with a database.
- **Tailwind** CSS framework.

## Libraries

### Instalation
``` bash
pip install fastapi uvicorn Jinja2 SQLAlchemy pytailwindcss
```
``` bash
tailwindcss
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
- `/requirements` files that lists all the Python dependencies needed.
- `/app` main source directory of this project. It contains the core logic of this application.
- `/models` SQLAlchemy models.
- `/routers` FastAPI routers / API endpoints.
- `/templates` all the HTML templates.
- `/styles` custom css styles.
- `/static` static CSS and JavaScript files, images etc.

### Files
- `.env` stores environment variables.
- `.gitignore` file to ignore files and directories.
- `README.md` project documentation.
- `main.py` entry point of the application where is an instance of the FastAPI class, routers linking and config.
