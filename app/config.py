import os
from dotenv import load_dotenv
from passlib.context import CryptContext

###################################
# Load .env File
###################################
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, '.env')
load_dotenv(ENV_PATH)

###################################
# JWT Config
###################################
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

###################################
# Password Hashing
###################################
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
