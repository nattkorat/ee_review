from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    level: int = 0  # Default level is 0

class UserOut(BaseModel):
    id: int
    username: str
    level: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
