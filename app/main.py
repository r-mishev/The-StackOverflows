from typing import Any, Dict
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from fastapi.middleware.cors import CORSMiddleware

from app.auth import authenticate_admin, create_access_token
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.routers import detection, ws, incoming_sms

def create_app() -> FastAPI:
    """
    Creates and configures the FastAPI application with routers and CORS middleware.
    """
    app = FastAPI()

    # Include the detection router (REST endpoints)
    app.include_router(detection.router, prefix="", tags=["detection"])
    app.include_router(incoming_sms.router, prefix="", tags=["sms"])
    # Include the WebSocket router
    app.include_router(ws.router, prefix="", tags=["websocket"])

    # Add CORS middleware for cross-origin requests from specific frontend
    app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://skyguardianfrontend.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

    @app.post("/login")
    def login(form_data: OAuth2PasswordRequestForm = Depends()):
        """
        OAuth2-based login for username/password authentication.
        Returns a JWT token if credentials are valid.
        """
        print("Received login request:", form_data.username)
        
        # Authenticate the admin credentials
        if not authenticate_admin(form_data.username, form_data.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Generate the access token with expiration time
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": form_data.username},
            expires_delta=access_token_expires
        )
        
        return {"access_token": access_token, "token_type": "bearer", "Access-Control-Allow-Origin": "*"}

    return app

# Create the app instance
app = create_app()
