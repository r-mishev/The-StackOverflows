from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

import app.config

from app.firebase import db

# Reuse the OAuth2PasswordBearer for token-based auth
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return app.config.pwd_context.verify(plain_password, hashed_password)

def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
):
    """
    Creates a JWT token with the given data as payload.
    We set "exp" for expiration and encode it with SECRET_KEY.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        app.config.SECRET_KEY,
        algorithm=app.config.ALGORITHM
    )
    return encoded_jwt

def authenticate_admin(username: str, password: str) -> bool:
    """
    Look up the admin in Firestore by username field, not by document ID.
    Verify the password, and return the admin record if valid.
    Otherwise return None.
    """
    # Query the "admins" collection where "username" == <username param>
    admins_ref = db.collection("admins")
    query = admins_ref.where("username", "==", username).limit(1)
    results = list(query.stream())
    
    # If no docs match, return None => "Incorrect username or password"
    if not results:
        return None
    
    # We found at least one doc
    doc = results[0]
    admin_data = doc.to_dict()  # e.g. { "username": "admin", "password_hash": "...", ... }

    hashed_pw = admin_data.get("password_hash")
    if not hashed_pw:
        return None

    if not verify_password(password, hashed_pw):
        return None
    
    return admin_data

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

    # Now do the same field-based lookup
    admins_ref = db.collection("admins")
    query = admins_ref.where("username", "==", username).limit(1)
    results = list(query.stream())
    
    if not results:
        raise credentials_exception  # No doc found => invalid token

    doc = results[0]
    admin_data = doc.to_dict()

    # Optionally check if admin_data is missing fields or is otherwise incomplete
    return admin_data