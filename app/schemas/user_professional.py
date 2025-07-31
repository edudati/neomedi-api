from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class UserProfessionalBase(BaseModel):
    bio: Optional[str] = None
    license_number: Optional[str] = None
    is_public: bool = True
    is_available: bool = True

class UserProfessionalCreate(UserProfessionalBase):
    user_id: UUID

class UserProfessionalUpdate(BaseModel):
    bio: Optional[str] = None
    license_number: Optional[str] = None
    is_public: Optional[bool] = None
    is_available: Optional[bool] = None

class UserProfessionalResponse(UserProfessionalBase):
    user_id: UUID

    class Config:
        from_attributes = True 