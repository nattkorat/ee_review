from pydantic import BaseModel, field_validator
from typing import List, Optional
import json

class CreateProject(BaseModel):
    name: str
    description: str | None = None

class ProjectOut(BaseModel):
    id: int
    name: str
    description: str | None = None

    class Config:
        from_attributes = True

class CreateTask(BaseModel):
    id: str
    project_id: int
    article: str
    events: str | None = None # JSON string to store events

class CreateReview(BaseModel):
    events: str | None = None  # JSON string to store events
    comment: str | None = None  # Optional field for reviewer comments
    
class ReviewOut(BaseModel):
    id: int
    task_id: str
    reviewer_id: int
    events: str | None = None  # JSON string to store events
    comment: str | None = None  # Optional field for reviewer comments

    class Config:
        from_attributes = True

class UploadFile(BaseModel):
    file: bytes  # Assuming the file is uploaded as bytes
    filename: str  # Name of the file being uploaded
    content_type: str  # MIME type of the file, e.g., 'text/csv', 'application/json'
    
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True  # Allow bytes as a type

class UploadFileResponse(BaseModel):
    content_type: str
    size: int  # Size of the uploaded file in bytes


class TaskOut(BaseModel):
    id: str
    project_id: int
    article: str
    events: list | None = None  # JSON string to store events
    status: bool | None = None
    
    @field_validator("events", mode="before")
    @classmethod
    def validate_events(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)  # Convert JSON string to dict
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON string for events")
        return v  # Already a dict or None

    class Config:
        from_attributes = True
        orm_mode = True  # Enable ORM mode for compatibility with SQLAlchemy models

class TaskListOut(BaseModel):
    tasks: List[TaskOut]
    total: int
    
class DonwloadFileResponse(BaseModel):
    filename: str
    content_type: str

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True  # Allow bytes as a type