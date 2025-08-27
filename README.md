# AbarWord Blog

A simple blog project built with FastAPI and SQLite.  
This project supports user authentication, post and category management, and file uploads.

---

## Features

- User registration and authentication
- CRUD operations for posts
- CRUD operations for categories
- File uploads for post images
- SQLite database with persistent storage via Docker volumes
- Session-based authentication

---

## Installation

1. Clone the repository:  
   ```bash
   git clone https://github.com/yourusername/abarword-blog.git
   cd abarword-blog
   ```
2. make `.env` file and config that.
3. Build and run using:
   - Docker:
    ```bash
    docker-compose up --build
    ```
   - Python:
    ```bash
    virtualenv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    python main.py
    ```
4. Access the application:
The API will be available at: `http://localhost:8000`

## Volumes

- `./data` → SQLite database  
- `./uploads` → Uploaded files (images, documents, etc.)

---

## API Endpoints

### Account

- **POST /account/** → Create a user

### Auth

- **POST /auth/login** → Login
- **POST /auth/logout** → Logout
- **GET /auth/me** → Get current user info

### Post

#### Categories

- **GET /post/category/list/** → List categories
- **POST /post/category/create/** → Create category
- **DELETE /post/category/delete/{id}** → Delete category

#### Posts

- **GET /post/post-list/** → List posts
- **GET /post/detail/{id}** → Get post detail
- **POST /post/create/** → Create post
- **PUT /post/update/{id}** → Update post
- **DELETE /post/delete/{id}** → Delete post

---

## File Uploads

- Uploaded files are stored in the `uploads/` folder.  
- Ensure the folder is writable by the application.

---

## Contributing

Contributions are welcome! Please create a pull request or open an issue.

---

## License

This project is licensed under the MIT License.
