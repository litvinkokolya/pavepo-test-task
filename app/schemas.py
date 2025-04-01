from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    yandex_id: Optional[str] = None
    full_name: Optional[str] = None


class UserCreate(UserBase):
    yandex_id: Optional[str] = None


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None


class UserInDB(UserBase):
    id: int
    is_active: bool
    is_superuser: bool

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    yandex_id: Optional[str] = None


class AudioFileBase(BaseModel):
    name: str


class AudioFileCreate(AudioFileBase):
    pass


class AudioFileInDB(AudioFileBase):
    id: int
    file_path: str
    owner_id: int

    class Config:
        orm_mode = True