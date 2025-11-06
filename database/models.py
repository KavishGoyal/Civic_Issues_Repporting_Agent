from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()

Base = declarative_base()

class CivicIssue(Base):
    __tablename__ = "civic_issues_types"
    
    id = Column(Integer, primary_key=True, index=True)
    reporter_name = Column(String(255))
    location = Column(String(500))
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    issue_type = Column(String(100))
    description = Column(Text)
    image_path = Column(String(500))
    audio_path = Column(String(500), nullable=True)
    status = Column(String(50), default="pending")
    priority = Column(String(20), default="medium")
    assigned_agency = Column(String(255))
    suggested_actions = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
class Agency(Base):
    __tablename__ = "agencies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True)
    department = Column(String(255))
    email = Column(String(255))
    phone = Column(String(50))
    issue_types = Column(JSON)
    
class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    issue_id = Column(Integer)
    agency_id = Column(Integer)
    message = Column(Text)
    status = Column(String(50), default="sent")
    created_at = Column(DateTime, default=datetime.utcnow)

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "") ## can provide the url directly 
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
