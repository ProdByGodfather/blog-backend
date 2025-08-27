import os

from fastapi import APIRouter, HTTPException, status, Request, Form

from post.models import Category
from account.models import User
from auth.session import get_user_from_request

router = APIRouter()



@router.get("/category/list/")
def category_list():
    return Category.all().to_dict()

@router.post("/category/create/")
def category_create(request: Request, title: str = Form(...)):
    user_id = get_user_from_request(request)
    user = User.filter(id = user_id).first()
    if not user or user.is_superuser == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Just Admins can create category")
    
    category = Category.filter(title=title).first()
    if category:
        raise HTTPException(status_code=400, detail="Category with this title already exists")
    
    Category.create(title=title)
    
    category = Category.filter(title=title).first()
    if not category:
        raise HTTPException(status_code=400, detail="Category creation failed")
    return {"id": category.id, "title": category.title}

@router.delete('/category/delete/{id}')
def category_delete(request: Request, id : int):
    user_id = get_user_from_request(request)
    user = User.filter(id = user_id).first()
    if not user or user.is_superuser == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Just Admins can create category")
    
    deleted = Category.delete(id = id)
    
    if deleted:
        return {"message": "deleted"}