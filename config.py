import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    # Render provides a URL that starts with "postgres://" — SQLAlchemy modern drivers accept
    # "postgresql://" — normalize just in case:
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
else:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL_LOCAL", "sqlite:///posts.db")
