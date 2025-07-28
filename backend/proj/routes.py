from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from backend.proj import schemas, crud, models
from backend.database import SessionLocal
from backend.auth.routes import get_current_user
from backend.auth.models import User

router = APIRouter(prefix="/projects")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("", response_model=list[schemas.ProjectOut])
def get_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    projects = crud.get_projects(db, owner_id=current_user.id, skip=skip, limit=limit)
    return projects

@router.post("", response_model=schemas.ProjectOut, status_code=status.HTTP_201_CREATED)
def create_project(project: schemas.CreateProject, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud.create_project(db, project, owner_id=current_user.id)

@router.get("/{project_id}", response_model=schemas.ProjectOut)
def get_project(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = crud.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.get("/{project_id}/tasks", response_model=list[schemas.TaskOut])
def get_tasks(project_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    tasks = crud.get_tasks(db, project_id=project_id, skip=skip, limit=limit)
    return tasks

@router.post("/{project_id}/tasks", response_model=schemas.TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(project_id: int, task: schemas.CreateTask, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    task.project_id = project_id
    return crud.create_task(db, task)

@router.get("/{project_id}/tasks/{task_id}", response_model=schemas.TaskOut)
def get_task(project_id: int, task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = crud.get_task(db, project_id=project_id, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.post(
    "/{project_id}/tasks/upload",
    response_model=schemas.UploadFileResponse,
    status_code=status.HTTP_201_CREATED,
)
def upload_task_file(
    project_id: int,
    file: UploadFile = File(...),  # ✅ Accept actual uploaded file from form
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not file:
        raise HTTPException(status_code=400, detail="No file provided")

    task = crud.create_task_from_file(db, project_id=project_id, file=file.file)

    if not task:
        raise HTTPException(status_code=400, detail="Failed to create task from file")

    return schemas.UploadFileResponse()

