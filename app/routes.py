from fastapi import APIRouter, Depends, HTTPException
from app.models import UserRegister, UserOut
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
