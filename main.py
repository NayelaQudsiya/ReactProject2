from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from uuid import UUID, uuid4
from typing import List

app = FastAPI()

# Define a User model
class User(BaseModel):
    id: UUID = uuid4()  # Automatically generate UUID
    name: str
    email: EmailStr
    password: str

# In-memory storage for users
users: List[User] = []

@app.post("/users/", response_model=User)
def create_user(user: User):
    users.append(user)
    return user

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "headers": dict(request.headers)},
    )

@app.get("/users/", response_model=List[User])
def get_users():
    return users

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: UUID):
    user = next((user for user in users if user.id == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: UUID, updated_user: User):
    user_index = next((i for i, user in enumerate(users) if user.id == user_id), None)
    if user_index is None:
        raise HTTPException(status_code=404, detail="User not found")
    users[user_index] = updated_user
    return updated_user

@app.delete("/users/{user_id}")
def delete_user(user_id: UUID):
    user_index = next((i for i, user in enumerate(users) if user.id == user_id), None)
    if user_index is None:
        raise HTTPException(status_code=404, detail="User not found")
    users.pop(user_index)
    return {"message": "User deleted successfully"}