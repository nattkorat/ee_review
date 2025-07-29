from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Query, status
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

@router.get("/{project_id}/tasks", response_model=schemas.TaskListOut)
def get_tasks(
    project_id: int,
    skip: int = 0,
    limit: int = 100,
    status: bool | None = Query(None),  # Optional filter
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    tasks, total = crud.get_tasks_with_total(
        db, project_id=project_id, skip=skip, limit=limit, status=status
    )
    return {"tasks": tasks, "total": total}

@router.get("/{project_id}/tasks/{task_id}", response_model=schemas.TaskOut)
def get_task(project_id: int, task_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = crud.get_task(db, task_id=task_id)
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

