from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, Integer, String
from app.database import Base

# ✅ SQLAlchemy User Table
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

# Request model for registering a user
class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str

# In-memory storage model (no password in response)
class UserOut(BaseModel):
    name: str
    email: EmailStr
