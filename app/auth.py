from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError

from app import config

# Reuse the OAuth2PasswordBearer for token-based auth
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return config.pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Creates a JWT token with the given data as payload.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return encoded_jwt

def authenticate_admin(username: str, password: str) -> bool:
    """
    Check if provided credentials match the hardcoded admin user in config.
    """
    if username != config.ADMIN_USERNAME:
        return False
    return verify_password(password, config.ADMIN_PASSWORD_HASH)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Dependency function that is used in protected routes to verify JWT.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # For a single admin user, confirm it's the admin
    if username != config.ADMIN_USERNAME:
        raise credentials_exception

    return username