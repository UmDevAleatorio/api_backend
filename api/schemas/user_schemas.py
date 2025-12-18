from pydantic import BaseModel, EmailStr, ConfigDict, field_validator
from typing import Optional, Any

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserResponse(UserBase):
    id: str

    model_config = ConfigDict(from_attributes=True)
    
    @field_validator('name', 'email', mode='before')
    @classmethod
    def extract_value_object(cls, v: Any) -> Any:
        if hasattr(v, 'value'):
            return v.value
        return v

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: str
    name: str