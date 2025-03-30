from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

import app.config
from app.firebase import db

# OAuth2PasswordBearer instance for token-based authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies if the provided plain password matches the hashed password.
    """
    return app.config.pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Generates a JWT token with the provided data as payload and expiration.
    """
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(
        to_encode,
        app.config.SECRET_KEY,
        algorithm=app.config.ALGORITHM
    )
    return encoded_jwt


def authenticate_admin(username: str, password: str) -> Optional[dict]:
    """
    Authenticates the admin by verifying the username and password.
    Returns admin data if valid, otherwise returns None.
    """
    admins_ref = db.collection("admins")
    query = admins_ref.where("username", "==", username).limit(1)
    results = list(query.stream())
    
    if not results:
        return None
    
    doc = results[0]
    admin_data = doc.to_dict()
    hashed_pw = admin_data.get("password_hash")
    
    if not hashed_pw or not verify_password(password, hashed_pw):
        return None
    
    return admin_data


async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Verifies the JWT token and returns the current admin's data.
    Raises HTTPException if token is invalid.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            token,
            app.config.SECRET_KEY,
            algorithms=[app.config.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    admins_ref = db.collection("admins")
    query = admins_ref.where("username", "==", username).limit(1)
    results = list(query.stream())
    
    if not results:
        raise credentials_exception

    doc = results[0]
    return doc.to_dict()
