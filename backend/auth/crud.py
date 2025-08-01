from sqlalchemy.orm import Session
from backend.auth import models
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, username: str, password: str, level: int = 0):
    hashed = pwd_context.hash(password)
    user = models.User(username=username, hashed_password=hashed)
    # check if there is users then set level to 1, otherwise set to 0
    existing_user = db.query(models.User).first()
    if existing_user:
        user.level = 1  # Set level to 1 if there are existing users
    else:
        user.level = level  # Set to provided level if no users exist
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
