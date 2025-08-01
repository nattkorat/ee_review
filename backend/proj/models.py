from sqlalchemy import Column, Integer, String, DateTime, Boolean
from backend.database import Base
from datetime import datetime

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, nullable=False)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    modified_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(String, primary_key=True, index=True)
    project_id = Column(Integer, nullable=False)
    article = Column(String, nullable=False)
    events = Column(String, nullable=True) # JSON string to store events
    created_at = Column(DateTime, default=datetime.utcnow)
    modified_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
 
    
class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String, nullable=False)
    reviewer_id = Column(Integer, nullable=False)
    events = Column(String, nullable=True)  # JSON string to store events
    comment = Column(String, nullable=True)  # Optional field for reviewer comments
    created_at = Column(DateTime, default=datetime.utcnow)
    modified_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
