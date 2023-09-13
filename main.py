from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

app = FastAPI()

# SQLAlchemy Setup
DATABASE_URL = "mysql+mysqlconnector://uche:password@localhost/hngdb_stage_two"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Define the Track model
class Track(Base):
    __tablename__ = "tracks"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), unique=True, index=True)


# Define the User model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    gender = Column(String(1), nullable=True)
    email = Column(String, nullable=True)
    username = Column(String(128), nullable=True)
    track_id = Column(Integer, ForeignKey("tracks.id"), nullable=True)
    stage = Column(Integer, default=0)
    date_created = Column(DateTime, default=datetime.utcnow)
    date_modified = Column(DateTime, onupdate=datetime.utcnow)
    is_deleted = Column(Boolean, default=False)

    # Define the relationship between User and Track
    track = relationship("Track", back_populates="users")


# Define the relationship between Track and User
Track.users = relationship("User", back_populates="track")


# Pydantic models for request and response
class UserCreate(BaseModel):
    name: str
    gender: str = None
    email: EmailStr = None
    username: str = None
    track_id: int = None


class UserUpdate(BaseModel):
    name: str
    gender: str = None
    email: EmailStr = None
    username: str = None
    track_id: int = None


class UserResponse(BaseModel):
    name: str
    gender: str = None
    email: EmailStr = None
    username: str = None
    track_id: int = None


# API endpoints for CRUD operations on User
@app.post("/api/", response_model=UserResponse)
def create_user(user: UserCreate):
    db = SessionLocal()
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db.close()
    return db_user


@app.get("/api/", response_model=List[UserResponse])
def get_all_users():
    db = SessionLocal()
    users = db.query(User).all()
    db.close()
    return users


@app.get("/api/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    db.close()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.put("/api/{user_id}", response_model=UserResponse)
def update_user(user_id: int, updated_user: UserUpdate):
    db = SessionLocal()
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")

    for field, value in updated_user.model_dump().items():
        setattr(db_user, field, value)

    db.commit()
    db.refresh(db_user)
    db.close()
    return db_user


@app.delete("/api/{user_id}", response_model=UserResponse)
def delete_user(user_id: int):
    db = SessionLocal()
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()
    db.close()
    return db_user
