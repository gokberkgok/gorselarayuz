"""
Database configuration — SQLAlchemy + MySQL (XAMPP)
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# MySQL connection via XAMPP (PyMySQL driver)
# Format: mysql+pymysql://user:password@host:port/database
DATABASE_URL = "mysql+pymysql://root:@localhost:3306/rezervasyon_db?charset=utf8mb4"

engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=3600)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency: yields a DB session, closes after use."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
