# CodeShare

CodeShare is a social media platform designed specifically for software developers. It allows users to share interesting code snippets, follow other users, and interact with posts.

## Technology Stack

- **FastAPI**: Used to build the main application and define all the APIs.
- **Uvicorn**: Serves the FastAPI application.
- **Jinja2**: Renders HTML templates for the frontend.
- **SQLAlchemy**: Connects with the database.
- **Tailwind CSS**: Provides utility-first CSS framework for rapid UI development.

## Installation

To install the required libraries, run the following command:

```bash
pip install fastapi uvicorn Jinja2 SQLAlchemy pytailwindcss passlib bcrypt python-multipart
```

To install Tailwind CSS, run:
``` bash
tailwindcss
```

### Run the app
``` bash
cd app
uvicorn main:app --reload
```
On the second terminal in the `/` directory run
``` bash
tailwindcss -i styles/main.css -o static/css/main.css --watch
```
Then go to the `http://localhost:8000/`


## Project structure

### Directories
- `/app`: Contains the core logic of the application.
- `/models`: Contains SQLAlchemy models.
- `/routers`: Contains FastAPI routers / API endpoints.
- `/templates`: Contains all the HTML templates.
- `/styles`: Contains custom CSS styles.
- `/static`: Contains static CSS and JavaScript files, images, etc.


### Files
- `requirements.txt`: Lists all the Python dependencies needed.
- `.env`: Stores environment variables.
- `.gitignore`: Specifies files and directories to ignore.
- `main.py`: Serves as the entry point of the application. It contains an instance of the FastAPI class, routers linking, and configuration.
- `crud.py`: 
