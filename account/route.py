# routes/user.py
import os
from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from config.settings import UPLOAD_DIR
from account.models import User
from account.schemas import UserCreate
from extensions.password_hasher import hash_password

router = APIRouter()

@router.post("/", response_model=UserCreate)
async def create_user(
    username: str = Form(...),
    password: str = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    image: UploadFile = File(None)
):
    # check username is unique
    if User.filter(username=username).exists():
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # save image if exists
    image_path = None
    if image:
        filename = f"{username}_{image.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        with open(file_path, "wb") as f:
            f.write(await image.read())
        image_path = f"/uploads/{filename}"  # just save image path

    # make user
    user = User.create(
        username=username,
        password=hash_password(password),  # hashing password
        first_name=first_name,
        last_name=last_name,
        email=email,
        image=image_path,
        is_superuser=False  # default
    )
    if user:
        return {
            "username": username,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "image": image_path
        }
        
    else:
        return HTTPException(status_code=400, detail={"error on save data"})