from sqlalchemy.orm import Session
from backend.proj import models, schemas
import csv
import json
import os
from io import StringIO


# project CRUD operations
def get_project(db: Session, project_id: int):
    return db.query(models.Project).filter(models.Project.id == project_id).first()

def get_projects(db: Session, owner_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Project).filter(models.Project.owner_id == owner_id).offset(skip).limit(limit).all()

def create_project(db: Session, project: schemas.CreateProject, owner_id: int):
    db_project = models.Project(**project.dict(), owner_id=owner_id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def update_project(db: Session, project_id: int, project: schemas.CreateProject):
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if db_project:
        for key, value in project.dict().items():
            setattr(db_project, key, value)
        db.commit()
        db.refresh(db_project)
        return db_project
    return None

def delete_project(db: Session, project_id: int):
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if db_project:
        db.delete(db_project)
        db.commit()
        return db_project
    return None

# task CRUD operations
def get_task(db: Session, task_id: str):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def get_tasks_with_total(db: Session, project_id: int, skip: int = 0, limit: int = 100, status: bool | None = None):
    query = db.query(models.Task).filter(models.Task.project_id == project_id)

    if status is not None:
        query = query.filter(models.Task.status == status)

    total = query.count()
    tasks = query.offset(skip).limit(limit).all()
    return tasks, total

def get_tasks(db: Session, project_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Task).filter(models.Task.project_id == project_id).offset(skip).limit(limit).all()

def create_task(db: Session, task: schemas.CreateTask):
    db_task = models.Task(
        id=task.id,  # Ensure id is set if provided
        project_id=task.project_id,
        article=task.article,  # Use 'article' for task content
        events=json.dumps(task.events),  # Convert events to JSON string
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: str, task: schemas.CreateTask):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task:
        for key, value in task.dict().items():
            setattr(db_task, key, value)
        db.commit()
        db.refresh(db_task)
        return db_task
    return None

def delete_task(db: Session, task_id: str):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()
        return db_task
    return None

def create_task_from_file(db: Session, project_id: int, file: bytes):
    if isinstance(file, bytes):
        file_content = file.decode('utf-8')
    else:
        file_content = file

    tasks = []
    # task can be only in JSONL format
    if file_content:
        # JSONL format
        for line in file_content:
            task_data = json.loads(line)
            tasks.append(task_data)
    else:
        # CSV format
        csv_reader = csv.DictReader(StringIO(file_content))
        for row in csv_reader:
            tasks.append(row)

    created_tasks = []
    for task_data in tasks:
        task_data['project_id'] = project_id  # Ensure project_id is set
        db_task = models.Task(
            project_id=project_id,
            id=task_data.get('id', None),  # Ensure id is set if provided
            article=task_data.get('text', None),  # Use 'text' for article content
            events=json.dumps(task_data['events']),  # Optional field
            status=task_data.get('status', False)  # Default to False if not provided
        )
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        created_tasks.append(db_task)

    return {
        "filename": file.name if hasattr(file, 'name') else "unknown",
        "content_type": "application/json",
        "size": len(tasks)
    }

# review CRUD operations
def get_review(db: Session, review_id: int):
    return db.query(models.Review).filter(models.Review.id == review_id).first()

def get_reviews(db: Session, task_id: str, skip: int = 0, limit: int = 100):
    return db.query(models.Review).filter(models.Review.task_id == task_id).offset(skip).limit(limit).all()

def create_review(db: Session, review: schemas.CreateReview, task_id: str, reviewer_id: int):
    db_review = models.Review(
        task_id=task_id,
        reviewer_id=reviewer_id,
        events=review.events,
        comment=review.comment,  # Optional field for reviewer comments
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    
    # update task status to completed
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task:
        db_task.status = True  # Mark task as completed
        db.commit()
        db.refresh(db_task)
    return db_review

def update_review(db: Session, review_id: int, review: schemas.CreateReview):
    db_review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if db_review:
        for key, value in review.dict().items():
            setattr(db_review, key, value)
        db.commit()
        db.refresh(db_review)
        return db_review
    return None

def delete_review(db: Session, review_id: int):
    db_review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if db_review:
        db.delete(db_review)
        db.commit()
        return db_review
    return None

def export_tasks_to_jsonl(db: Session, project_id: int) -> str:
    # Only get tasks that are completed
    tasks = db.query(models.Task).filter(models.Task.project_id == project_id, models.Task.status == True).all()
    
    file_path = f"./exports/project_{project_id}_reviews.jsonl"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, 'w', encoding='utf-8') as f:
        for task in tasks:
            # Get the most recent review for this task
            review = (
                db.query(models.Review)
                .filter(models.Review.task_id == task.id)
                .order_by(models.Review.created_at.desc())
                .first()
            )

            row = {
                "id": task.id,
                "article": task.article,
                "events": json.loads(review.events) if review else None,
                "comment": review.comment if review else None,
            }
            f.write(json.dumps(row, ensure_ascii=False) + '\n')

    return file_path