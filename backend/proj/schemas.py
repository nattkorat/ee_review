from pydantic import BaseModel

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
    
class TaskOut(BaseModel):
    id: str
    project_id: int
    article: str
    events: str | None = None
    status: bool = False  # True for completed, False for pending

    class Config:
        from_attributes = True

class CreateReview(BaseModel):
    task_id: str
    reviewer_id: int
    events: str | None = None  # JSON string to store events
    
class ReviewOut(BaseModel):
    id: int
    task_id: str
    reviewer_id: int
    events: str | None = None  # JSON string to store events

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
    filename: str
    content_type: str
    size: int  # Size of the uploaded file in bytes

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True  # Allow bytes as a type

class TaskOut(BaseModel):
    id: str
    project_id: int
    article: str
    events: str | None = None  # JSON string to store events
    status: bool = False  # True for completed, False for pending

    class Config:
        from_attributes = True
        orm_mode = True  # Enable ORM mode for compatibility with SQLAlchemy models