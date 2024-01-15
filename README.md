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
pip install -r requirements.txt
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
- `.gitignore`: Specifies files and directories that Git should ignore.
- `LICENSE`: The license for the project.
- `README.md`: The main documentation file for the project.
- `requirements.txt`: Lists all the Python dependencies needed for the project.
- `tailwind.config.js`: Configuration file for Tailwind CSS.
- `app/`: Contains the core logic of the application.
    - `crud/`: Contains the CRUD operations for different entities.
        - `crud_comment.py`: Contains CRUD operations for comments.
        - `crud_follow.py`: Contains CRUD operations for follows.
        - `crud_like.py`: Contains CRUD operations for likes.
        - `crud_post.py`: Contains CRUD operations for posts.
        - `crud_user.py`: Contains CRUD operations for users.
    - `database.py`: Handles database connections and sessions.
    - `main.py`: Serves as the entry point of the application. It contains an instance of the FastAPI class, routers linking, and configuration.
    - `models/`: Contains SQLAlchemy models.
        - `comment.py`: Defines the Comment model.
        - `follower.py`: Defines the Follower model.
        - `post.py`: Defines the Post model.
        - `post_like.py`: Defines the PostLike model.
        - `user.py`: Defines the User model.
    - `routers/`: Contains FastAPI routers / API endpoints.
        - `feed.py`: Defines the endpoints for the feed.
        - `follow.py`: Defines the endpoints for following users.
        - `like.py`: Defines the endpoints for liking posts.
        - `login.py`: Defines the endpoints for user login and logout.
        - `register.py`: Defines the endpoints for user registration.
        - `user.py`: Defines the endpoints for user profile and settings.
        - `post.py`: Defines the endpoints for creating, updating.
        - `comment.py`: Defines the endpoints for creating
        - `schemas.py`: Contains Pydantic schemas for data validation.
- `static/`: Contains static CSS and JavaScript files, images, etc.
    - `css/`: Contains CSS files.
    - `images/`: Contains image files.
    - `js/`: Contains JavaScript files.
- `styles/`: Contains custom CSS styles.
    - `main.css`: The main CSS file.
- `templates/`: Contains all the HTML templates.
    - `components/`: Contains reusable HTML components.
    - `error.html`: The error page template.
    - `feed.html`: The feed page template.
    - `index.html`: The home page template.
    - `login.html`: The login page template.
    - `post_detailed.html`: The detailed post page template.
    - `register.html`: The registration page template.
    - `user.html`: The user profile page template.
    - `user_settings.html`: The user settings page template.