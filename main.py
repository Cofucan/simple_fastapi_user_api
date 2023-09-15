""" A simple FastAPI CRUD app """
from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Boolean,
    func,
)
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# from config import MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DB
from config import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB

app = FastAPI()

db_user = POSTGRES_USER
db_password = POSTGRES_PASSWORD
db_host = POSTGRES_HOST
db_name = POSTGRES_DB
db_port = POSTGRES_PORT

# Database Setup
# DATABASE_URL = f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{server_ip}:{port}/{db_name}"
DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
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
    email = Column(String, unique=True, nullable=True)
    username = Column(String(128), unique=True, nullable=True)
    track_id = Column(Integer, ForeignKey("tracks.id"), nullable=True)
    stage = Column(Integer, default=0)
    date_created = Column(DateTime, server_default=func.now())
    date_modified = Column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )
    is_deleted = Column(Boolean, default=False)

    # Define the relationship between User and Track
    track = relationship("Track", back_populates="users")


# Define the relationship between Track and User
Track.users = relationship("User", back_populates="track")


# Pydantic models for request and response
class UserCreate(BaseModel):
    name: str
    gender: Optional[str] = None
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    track_id: Optional[int] = None


class UserUpdate(BaseModel):
    name: Optional[str] = None
    gender: Optional[str] = None
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    track_id: Optional[int] = None


class UserResponse(BaseModel):
    id: int
    name: str
    gender: Optional[str] = None
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    track_id: Optional[int] = None
    date_modified: Optional[datetime] = None


# Pydantic model for filtering criteria
class UserFilter(BaseModel):
    name: Optional[str] = None
    stage: Optional[int] = None
    gender: Optional[str] = None
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    track_id: Optional[int] = None


# API endpoints for CRUD operations on User
@app.post("/api/", response_model=UserResponse)
def create_user(user: UserCreate):
    """
    Create a new user in the database.

    Parameters:
        user (UserCreate): The user data to create.

    Returns:
        User: The created user.
    """
    db = SessionLocal()
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db.close()
    return db_user


# API endpoint to get users with filtering criteria
@app.get("/api/", response_model=List[UserResponse])
def get_users(filter_criteria: Optional[UserFilter] = None):
    """
    Retrieves a list of users from the database based on the provided filter
    criteria.

    Parameters:
    - filter_criteria (Optional[UserFilter]): The filter criteria to apply to
    the query. Defaults to None.

    Returns:
    - List[UserResponse]: A list of UserResponse objects representing the
    retrieved users.
    """
    db = SessionLocal()

    # Build the filter conditions based on the JSON request
    filter_conditions = []
    if filter_criteria:
        if filter_criteria.name:
            filter_conditions.append(User.name == filter_criteria.name)
        if filter_criteria.stage is not None:
            filter_conditions.append(User.stage == filter_criteria.stage)
        if filter_criteria.gender:
            filter_conditions.append(User.gender == filter_criteria.gender)
        if filter_criteria.email:
            filter_conditions.append(User.email == filter_criteria.email)
        if filter_criteria.username:
            filter_conditions.append(User.username == filter_criteria.username)
        if filter_criteria.track_id is not None:
            filter_conditions.append(User.track_id == filter_criteria.track_id)

    # Add the condition to filter out deleted users
    filter_conditions.append(User.is_deleted == False)

    # Apply the filter conditions to the query
    users = db.query(User).filter(*filter_conditions).all()

    db.close()
    return users


@app.get("/api/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    """
    Get a user from the database by their ID.

    Args:
        user_id (int): The ID of the user to retrieve.

    Returns:
        UserResponse: The user object.

    Raises:
        HTTPException: If the user is not found or has been deleted.
    """
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    db.close()
    if user is None or user.is_deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.put("/api/{user_id}", response_model=UserResponse)
def update_user(user_id: int, updated_user: UserUpdate):
    """
    Updates a user in the API.

    Args:
        user_id (int): The ID of the user to be updated.
        updated_user (UserUpdate): The updated user data.

    Returns:
        UserResponse: The updated user.

    Raises:
        HTTPException: If the user is not found.
    """
    db = SessionLocal()
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None or db_user.is_deleted:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")

    if updated_user.name is not None:
        db_user.name = updated_user.name
    if updated_user.gender is not None:
        db_user.gender = updated_user.gender
    if updated_user.email is not None:
        db_user.email = updated_user.email
    if updated_user.username is not None:
        db_user.username = updated_user.username
    if updated_user.track_id is not None:
        db_user.track_id = updated_user.track_id

    db.commit()
    db.refresh(db_user)
    db.close()
    return db_user


@app.delete("/api/{user_id}", response_model=UserResponse)
def delete_user(user_id: int):
    """
    Deletes a user from the database.

    Parameters:
        user_id (int): The ID of the user to be deleted.

    Returns:
        UserResponse: The deleted user object.

    Raises:
        HTTPException: If the user is not found in the database.
    """
    db = SessionLocal()
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")

    db_user.is_deleted = True
    db.commit()
    db.refresh(db_user)
    db.close()
    return db_user
