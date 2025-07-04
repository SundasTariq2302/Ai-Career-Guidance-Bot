from pydantic import BaseModel, EmailStr

# Request model for registering a user
class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str

# In-memory storage model (no password in response)
class UserOut(BaseModel):
    name: str
    email: EmailStr
