from fastapi import FastAPI
from app.database import Base, engine
from app.routes import auth, threads, posts, comments

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to my API 🚀"}
# Create tables
Base.metadata.create_all(bind=engine)

# Register Routers
app.include_router(auth.router)
app.include_router(threads.router)
app.include_router(posts.router)
app.include_router(comments.router)
