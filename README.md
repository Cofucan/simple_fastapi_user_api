# FastAPI User Management API

A simple RESTful API for user management built with FastAPI and SQLAlchemy. This API provides basic CRUD operations for managing user records in a MySQL database. It also supports filtering and querying users based on various criteria.

## Table of Contents

- Features
- Prerequisites
- Installation
- Usage
- API Endpoints
- Request and Response Formats
- Sample Usage
- Known Limitations
- Contributing
- License

## Features

- Create a new user
- Retrieve user details by ID
- Update user information
- Delete a user
- List all users with optional filtering criteria
- Automatic timestamps for date_created and date_modified
- Soft deletion with is_deleted flag

## Prerequisites

Before running the application, ensure you have the following prerequisites installed:

- Python 3.7 or higher
- MySQL database server
- MySQL connector for Python (install with pip install mysql-connector-python)
- FastAPI and SQLAlchemy (install with pip install fastapi sqlalchemy)

## Installation

1. Clone the repository:

    ```shell
   git clone https://github.com/yourusername/fastapi-user-management.git
    ```

2. Change to the project directory:

```shell
cd fastapi-user-management
```

3. Create a virtual environment (optional but recommended):

```shell
python -m venv venv
```

4. Activate the virtual environment:

```shell
venv\Scripts\activate
```

5. Install project dependencies:

```shell
pip install -r requirements.txt
```

6. Configure the database:

- Update the `DATABASE_URL` variable in the `main.py` file to point to your MySQL database.

7. Run the application:

```shell
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be accessible at http://localhost:8000.

## Usage

### API Endpoints

The API provides the following endpoints:

- `POST /api/`: Create a new user.
- `GET /api/`: List all users with optional filtering criteria.
- `GET /api/{user_id}`: Retrieve user details by ID.
- `PUT /api/{user_id}`: Update user information.
- `DELETE /api/{user_id}`: Delete a user.

### Request and Response Formats

UserCreate (Request Payload for Creating a User)

- `name` (str, required): User's name.
- `gender` (str, optional): User's gender ('M' for Male, 'F' for Female, 'O' for Other).
- `email` (str, optional): User's email address.
- `username` (str, optional): User's username.
- `track_id` (int, optional): ID of the user's track.

UserUpdate (Request Payload for Updating a User)

- `name` (str, optional): User's name.
- `gender` (str, optional): User's gender.
- `email` (str, optional): User's email address.
- `username` (str, optional): User's username.
- `track_id` (int, optional): ID of the user's track.

UserResponse (Response Format for User Details)

- `id` (int): User ID.
- `name` (str): User's name.
- `gender` (str, optional): User's gender.
- `email` (str, optional): User's email address.
- `username` (str, optional): User's username.
- `track_id` (int, optional): ID of the user's track.
- `date_modified` (datetime, optional): Timestamp of the last modification.

UserFilter (Request Payload for Filtering Users)
- `name` (str, optional): Filter users by name.
- `stage` (int, optional): Filter users by stage.
- `gender` (str, optional): Filter users by gender.
- `email` (str, optional): Filter users by email.
- `username` (str, optional): Filter users by username.
- `track_id` (int, optional): Filter users by track ID.

### Sample Usage

Create a New User: This ONLY required parameter to this endpoint is the `name`. All other parameters are not required. If they are not specified, they will be set to `null`.

> POST /api/

```json
{
  "name": "John Doe",
  "gender": "M",
  "email": "johndoe@example.com",
  "username": "johndoe123",
  "track_id": 1
}
```

Response:

```json
{
  "id": 1,
  "name": "John Doe",
  "gender": "M",
  "email": "johndoe@example.com",
  "username": "johndoe123",
  "track_id": 1, 
  "date_modified": "2023-09-13T12:34:56.789Z"
}
```

Get Users with Filtering Criteria: This fetches all users that match the criteria specified in the json request.
If no attribute is specified, then it returns all the users.

> GET /api/

```json
{
  "gender": "M"
}
```

Response:

```json
[
  {
    "id": 1,
    "name": "John Doe",
    "gender": "M",
    "email": "johndoe@example.com",
    "username": "johndoe123",
    "track_id": 1,
    "date_modified": "2023-09-13T12:34:56.789Z"
  },
  {
     "id": 4,
     "name": "William Dean",
     "gender": "M",
     "email": "williamdean@example.com",
     "username": "williamabc",
     "track_id": 3,
     "date_modified": "2023-09-13T12:34:56.789Z"
  }
]
```
