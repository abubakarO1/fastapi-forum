# Forum API (FastAPI + PostgreSQL)

A simple forum backend built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**.  
Users can register, log in, create threads, post replies, and comment on posts.  
Authentication is handled with JWT tokens.

---

## 🚀 Features
- User registration & login (JWT authentication)
- Create, read, update, delete:
  - Threads
  - Posts
  - Comments
- Secure password hashing with `bcrypt`
- Database integration with PostgreSQL
- Token-based authentication

---

## 🛠️ Tech Stack
- [FastAPI] – web framework
- [SQLAlchemy] – ORM
- [PostgreSQL] – database
- [Pydantic] – data validation
- [Passlib] – password hashing
- [Python-Jose] – JWT tokens
- [Uvicorn] – ASGI server

---

## 📂 Project Structure

<img width="455" height="379" alt="image" src="https://github.com/user-attachments/assets/8ea1c2f2-7ea6-4810-be06-9d2ac3027564" />



---

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/your-username/forum-api.git
cd forum-api

### 2. Create and activate a virtual environment

python -m venv venv
# On Windows
venv\Scripts\activate
# On Linux/Mac
source venv/bin/activate

### 3. Install dependencies

pip install -r requirements.txt

### 4. Run the server

uvicorn app.main:app --reload
Server will run on: http://127.0.0.1:8000

### 5. 🔑 API Endpoints
Auth

POST /auth/register → Register new user

POST /auth/login → Login & get JWT token

Threads

POST /threads/ → Create a new thread (auth required)

GET /threads/ → Get all threads

GET /threads/{id} → Get single thread with posts & comments

Posts

POST /threads/{thread_id}/posts/ → Create post under a thread

GET /threads/{thread_id}/posts/ → Get all posts in a thread

Comments

POST /posts/{post_id}/comments/ → Add comment under a post

GET /posts/{post_id}/comments/ → Get all comments for a post
