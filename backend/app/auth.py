from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from pathlib import Path

# 👇 Explicit path to .env (FIXES WINDOWS ISSUES)
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

SECRET = "supersecretkey123"

ALGORITHM = "HS256"


pwd = CryptContext(schemes=["bcrypt"])
def hash_password(p):
    return pwd.hash(p)

def verify_password(p, h):
    return pwd.verify(p, h)

def create_token(email):
    payload = {
        "sub": email,
        "exp": datetime.utcnow() + timedelta(hours=2)
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")
