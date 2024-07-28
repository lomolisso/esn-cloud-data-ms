from app.core.config import DATABASE_USER, DATABASE_PASS, DATABASE_HOST, DATABASE_PORT, DATABASE_NAME
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# --- Init DB ---
db_url = "postgresql://{0}:{1}@{2}:{3}/{4}".format(DATABASE_USER, DATABASE_PASS, DATABASE_HOST, DATABASE_PORT, DATABASE_NAME)
engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
