from fastapi import APIRouter, Depends, HTTPException
from app.models import UserRegister, UserOut
from app.services import hash_password, verify_password
from app.auth import create_access_token, get_current_user

router = APIRouter()

# Temporary DB
users_db = {}

@router.get("/status")
async def get_status():
    return {"status": "OK", "message": "Career Bot API running smoothly"}

# ✅ Register Route
@router.post("/register", response_model=UserOut)
async def register(user: UserRegister):
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_pw = hash_password(user.password)
    users_db[user.email] = {
        "name": user.name,
        "email": user.email,
        "password": hashed_pw,
    }

    return {"name": user.name, "email": user.email}

#  Login Route
@router.post("/login")
async def login(user: UserRegister):
    db_user = users_db.get(user.email)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid password")

    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

#  Protected Profile Route
@router.get("/profile")
async def get_profile(current_user_email: str = Depends(get_current_user)):
    user = users_db.get(current_user_email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"name": user["name"], "email": user["email"]}
