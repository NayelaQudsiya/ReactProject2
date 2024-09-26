from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import UUID, uuid4
from typing import List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow requests from React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the actual React domain instead of "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define a User model
class User(BaseModel):
    id: UUID = uuid4()  # Automatically generate UUID
    name: str
    email: str
    password: str

# In-memory storage for users
users: List[User] = []

@app.post("/send-message/")
def send_message(data: dict):
    message = data.get("message", "")
    if not message:
        raise HTTPException(status_code=400, detail="Message is required")
    
    return {"response": f"Thanks for sending the message: {message}"}
