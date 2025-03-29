import os
from dotenv import load_dotenv
from passlib.context import CryptContext

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, '.env')

load_dotenv(ENV_PATH)  # Load the .env file

SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD_HASH = os.getenv("ADMIN_PASSWORD_HASH", "$2b$12$...")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
