from fastapi import APIRouter, Depends, HTTPException
from app.models import UserRegister, UserOut, RecommendationRequest
from app.services import hash_password, verify_password
from app.auth import create_access_token, get_current_user
from sqlalchemy.orm import Session
from fastapi import Depends
from app.database import get_db
from app.models import User
from app.services import hash_password

router = APIRouter()

# Temporary DB
users_db = {}

@router.get("/status")
async def get_status():
    return {"status": "OK", "message": "Career Bot API running smoothly"}

# ✅ Register Route
@router.post("/register", response_model=UserOut)
async def register(user: UserRegister, db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")

    # Save user to DB
    new_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"name": new_user.name, "email": new_user.email}

#  Login Route
@router.post("/login")
async def login(user: UserRegister, db: Session = Depends(get_db)):
    # Check if user exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # Verify password
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # Generate JWT
    token = create_access_token({"sub": user.email})

    return {"access_token": token, "token_type": "bearer"}


#  Protected Profile Route
@router.get("/profile")
def get_profile(db: Session = Depends(get_db), user_email: str = Depends(get_current_user)):
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"name": user.name, "email": user.email}

# Example simple career mapping (you will improve it later)
# career_db = {
#     "Machine Learning Engineer": ["Python", "Machine Learning", "Deployment"],
#     "Data Scientist": ["Python", "Statistics", "Visualization"],
#     "AI Researcher": ["Deep Learning", "NLP", "Research"]
# }

# improved:
career_db = {
    "Machine Learning Engineer": {
        "keywords": ["Python", "Machine Learning", "Deployment"],
        "description": "Design and deploy machine learning models in production.",
        "next_steps": ["Learn TensorFlow", "Practice on cloud platforms (AWS, Azure)"]
    },
    "Data Scientist": {
        "keywords": ["Python", "Statistics", "Visualization"],
        "description": "Analyze and visualize data to solve business problems.",
        "next_steps": ["Master Pandas and Matplotlib", "Learn SQL"]
    },
    "AI Researcher": {
        "keywords": ["Deep Learning", "NLP", "Research"],
        "description": "Work on cutting-edge AI models and publish research.",
        "next_steps": ["Study advanced ML papers", "Contribute to open-source AI libraries"]
    }
}



# ✅ NEW: Recommend route
@router.post("/recommend")
def recommend_career(user: RecommendationRequest):
    recommendations = []

    for career, details in career_db.items():
        keywords = details["keywords"]

        # Score how many keywords match
        matched_keywords = set(user.skills + user.interests) & set(keywords)
        score = len(matched_keywords)

        if score > 0:
            recommendations.append({
                "career": career,
                "description": details["description"],
                "matched_skills": list(matched_keywords),
                "recommended_next_steps": details["next_steps"]
            })

    if not recommendations:
        return {"message": "No matching career found. Try expanding your skills and interests."}

    return {
        "name": user.name,
        "recommendations": recommendations
    }
