import os

from fastapi import APIRouter, Depends, HTTPException, status, Request, Form, File, UploadFile
from typing import Optional

from post.models import Post, Category
from post.schemas import PostListFilter, PostResponseSchema
from account.models import User
from auth.session import get_user_from_request
from config.settings import UPLOAD_DIR
from extensions.file_uploader import save_upload_file

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


@router.get("/post-list/")
def post_list(page: int = 1, page_size: int = 10, filters: PostListFilter = Depends() ):
    filter_kwargs = {}
    if filters.category_id is not None:
        filter_kwargs["category"] = filters.category_id
    if filters.author_id is not None:
        filter_kwargs["author"] = filters.author_id
    
    if filter_kwargs:
        query = Post.filter(**filter_kwargs)
    else:
        query = Post.all()
    
    if filters.search:
        query = query.contains(title = filters.search)
        
    if filters.ordering:
        query = query.order_by(filters.ordering)
    
    
    paginated_result = query.paginate(page=page, page_size=page_size)
    
    return paginated_result

@router.get('/detail/{id}')
def post_detail(id):
    post = Post.filter(id = id).first()
    if not post:
        raise HTTPException(status_code=404, detail="no post found")
    return post

@router.post("/create/", response_model=PostResponseSchema)
async def post_create(request: Request, 
    title: str = Form(...),
    description: str = Form(...),
    category_id: Optional[int] = Form(None),
    image: Optional[UploadFile] = File(None),):
    """
    - ایجاد یک پست جدید
    - کاربر باید لاگین کرده باشد (Session)
    """
    user_id = get_user_from_request(request)
    user = User.filter(id = user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")

    category = None
    if category_id:
        category = Category.get(id=category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
    
    if image:
        filename = f"{user.username}_{image.filename}"
        image_path = os.path.join(UPLOAD_DIR, filename)

        contents = await image.read()
        with open(image_path, "wb") as f:
            f.write(contents)

        image_path = f"/uploads/{filename}"
    else:
        raise HTTPException(status_code=400, detail="Image Needed")
    
    post = Post.filter(title=title, author=user.id).first()
    if post:
        raise HTTPException(status_code=400, detail="Post with this title already exists")
    
    Post.create(
        title=title,
        description=description,
        image=image_path,
        category=category.id,
        author=user.id
    )
    post = Post.filter(title=title, author=user.id).first()
    
    if not post:
        raise HTTPException(status_code=400, detail="Post creation failed")

    return PostResponseSchema(
        id=post.id,
        title=post.title,
        description=post.description,
        image=post.image,
        category=category.title if category else None,
        author=user.username,
        create_time=str(post.create_time)
    )

@router.delete('/delete/{id}')
def post_delete(request: Request, id: int):
    user_id = get_user_from_request(request)
    user = User.filter(id=user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")

    post = Post.filter(id=id, author=user_id).first()
    if not post:
        raise HTTPException(status_code=403, detail="You don't have delete permission.")

    Post.delete(id=post.id)  
    
    return {'detail': 'successful.'}


@router.put('/update/{id}')
def post_update(request: Request, id: int,
    title: str = Form(...),
    description: str = Form(...),
    category_id: Optional[int] = Form(None),
    image: Optional[UploadFile] = File(None)):
    """
    - بروز رسانی پست
    - کاربر باید لاگین کرده باشد (Session)
    """
    user_id = get_user_from_request(request)
    user = User.filter(id = user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    
    post = Post.filter(id=id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    if post.author != user.id and not user.is_staff:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to update this post")

    post.title = title
    post.description = description
    if category_id:
        post.category = category_id
    
    if image:
        post.image = save_upload_file(image)

    post.save()

    return {"status": "success", "message": "Post updated successfully", "post_id": post.id}

