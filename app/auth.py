from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import Depends, HTTPException
# from fastapi.security import OAuth2PasswordBearer
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Same values from before
SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"

# OAuth2 scheme for token extraction
oauth2_scheme = HTTPBearer()
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Create JWT token (as before)
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ✅ Decode and verify token
def get_current_user(token: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    try:
        # ✅ Extract the token string from HTTPAuthorizationCredentials
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        return email
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")