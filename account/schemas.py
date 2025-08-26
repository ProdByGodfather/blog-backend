from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str
    email: EmailStr
    image: Optional[str] = None  # مسیر عکس آپلود شده
