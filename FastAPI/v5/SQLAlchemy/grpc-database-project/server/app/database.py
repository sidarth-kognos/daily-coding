# ================================
# app/database.py
from sqlalchemy import Column, Integer, BigInteger, String, Text, DateTime, Float, JSON, ForeignKey,text,CheckConstraint
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
import structlog
from .config import settings

logger = structlog.get_logger()

# Create SQLAlchemy engine
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=False
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

class person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    email = Column(String(100), nullable=False,server_default=text("'not specified'"))
    salary=Column(Integer, nullable=False)
    manager_id = Column(Integer, ForeignKey('person.id'), nullable=True)
    department_id=Column(Integer, ForeignKey('department.id'),nullable=True)

class Department(Base):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    head = Column(String(100), nullable=True)

@contextmanager
def get_db_session() -> Session:
    """Context manager for database sessions"""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error("Database session error", error=str(e))
        raise
    finally:
        session.close()

def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

