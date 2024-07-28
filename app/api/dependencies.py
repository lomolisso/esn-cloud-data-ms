from app.db import SessionLocal

def get_session():
    """
    Database dependency for FastAPI
    """
    with SessionLocal() as session:
        yield session