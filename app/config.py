import os
from dotenv import load_dotenv
from passlib.context import CryptContext

# Load the .env file
load_dotenv()

# Load the values from the .env file
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD_HASH = os.getenv("ADMIN_PASSWORD_HASH")  # This will get the hash from the .env file
ALGORITHM = os.getenv("ALGORITHM")

# Initialize the bcrypt context for password hashing/verification
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Optionally, you can define `hashed_admin_password` here if it's missing in the .env file
# For testing purposes, this can be hardcoded
# ADMIN_PASSWORD_HASH = "$2b$12$EEXAMPLEhashhereWlfCVKjTGfa3m/7uSmQ"  # Replace this with the correct hash for testing
