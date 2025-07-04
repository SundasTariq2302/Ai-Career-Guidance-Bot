from fastapi import FastAPI
from app.routes import router  # We'll create routes.py next

app = FastAPI(title="AI Career Guidance Bot 🚀")

# Include all routes
app.include_router(router)

# Optional: Root route (just for testing)
@app.get("/")
def read_root():
    return {"message": "AI Career Bot is running 🚀"}
