import os
from dotenv import load_dotenv

load_dotenv()  # 👈 THIS LINE IS THE FIX

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

