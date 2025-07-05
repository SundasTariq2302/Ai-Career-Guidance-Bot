from fastapi import FastAPI
from app import routes  # We'll create routes.py next
from app.database import engine
from app.models import Base

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="AI Career Guidance Bot 🚀")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace "*" with your frontend's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routes
app.include_router(routes.router)

# Optional: Root route (just for testing)
@app.get("/")
def read_root():
    return {"message": "AI Career Bot is running 🚀"}

#  Create tables at startup
Base.metadata.create_all(bind=engine)

