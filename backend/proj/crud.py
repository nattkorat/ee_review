from sqlalchemy.orm import Session
from backend.proj import models, schemas
from sqlalchemy.orm import aliased
from sqlalchemy.sql import exists
from sqlalchemy import func
from collections import defaultdict
import csv
import json
import os
from io import StringIO


# project CRUD operations
def get_project(db: Session, project_id: int):
    return db.query(models.Project).filter(models.Project.id == project_id).first()

def get_projects(db: Session, owner_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Project).offset(skip).limit(limit).all()

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

def get_tasks_with_total(
    db: Session,
    user_id: int,
    project_id: int,
    skip: int = 0,
    limit: int = 100,
    status: bool | None = None,
):
    from sqlalchemy.sql import exists

    # Base query
    base_query = db.query(models.Task).filter(models.Task.project_id == project_id)

    # Subquery to check if review exists for task by this user
    review_exists_subq = (
        db.query(models.Review)
        .filter(
            models.Review.reviewer_id == user_id,
            models.Review.task_id == models.Task.id,
        )
    )

    if status is not None:
        if status:  # Reviewed
            base_query = base_query.filter(review_exists_subq.exists())
        else:  # Not reviewed
            base_query = base_query.filter(~review_exists_subq.exists())

    total = base_query.count()
    tasks = base_query.offset(skip).limit(limit).all()

    # Add status field to each task
    reviewed_task_ids = {
        r.task_id
        for r in db.query(models.Review.task_id)
        .filter(models.Review.reviewer_id == user_id)
        .all()
    }

    # Attach a transient `status` field (True if reviewed, False if not)
    for task in tasks:
        task.status = task.id in reviewed_task_ids

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
        )
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        created_tasks.append(db_task)

    return {
        "content_type": "application/json",
        "size": len(tasks)
    }

# review CRUD operations
def get_review(db: Session, review_id: int):
    return db.query(models.Review).first()

def get_review_by_owner(db: Session, owner_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Review).filter(models.Review.reviewer_id == owner_id).first()

def get_reviews(db: Session, task_id: str, skip: int = 0, limit: int = 100):
    return db.query(models.Review).filter(models.Review.task_id == task_id).offset(skip).limit(limit).all()

def get_reviews_by_owner(db: Session, owner_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Review).filter(models.Review.reviewer_id == owner_id).offset(skip).limit(limit).all()

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
    project_title = db.query(models.Project.name).filter(models.Project.id == project_id).scalar()
    safe_title = project_title.replace(" ", "_").lower()
    file_path = f"./exports/project_{safe_title}_reviews.jsonl"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    tasks = db.query(models.Task).filter(models.Task.project_id == project_id).all()

    # Subquery to get latest review per user per task
    sub_latest = (
        db.query(
            models.Review.task_id,
            models.Review.reviewer_id,
            func.max(models.Review.created_at).label("latest_time")
        )
        .group_by(models.Review.task_id, models.Review.reviewer_id)
        .subquery()
    )

    # Join to get full review info
    LatestReview = aliased(models.Review)
    latest_reviews = (
        db.query(LatestReview)
        .join(
            sub_latest,
            (LatestReview.task_id == sub_latest.c.task_id) &
            (LatestReview.reviewer_id == sub_latest.c.reviewer_id) &
            (LatestReview.created_at == sub_latest.c.latest_time)
        )
        .all()
    )

    # Group reviews by task_id
    reviews_by_task = defaultdict(list)
    for review in latest_reviews:
        reviews_by_task[review.task_id].append({
            "reviewer_id": review.reviewer_id,
            "events": json.loads(review.events) if review.events else None,
            "comment": review.comment,
        })

    # Write each task and its reviews
    with open(file_path, 'w', encoding='utf-8') as f:
        for task in tasks:
            row = {
                "id": task.id,
                "article": task.article,
                "original_events": json.loads(task.events) if task.events else None,
                "reviewed_events": reviews_by_task.get(task.id, [])
            }
            if row["reviewed_events"]:
                f.write(json.dumps(row, ensure_ascii=False) + '\n')

    return file_path
