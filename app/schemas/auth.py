from pydantic import BaseModel, EmailStr
from datetime import datetime


class SignupRequest(BaseModel):
    email: EmailStr
    firebase_uid: str
    firebase_token: str  # ID token do Firebase


class SignupResponse(BaseModel):
    id: int
    email: str
    firebase_uid: str
    created_at: datetime
    is_active: bool
    message: str


class AuthError(BaseModel):
    detail: str
    error_code: str 