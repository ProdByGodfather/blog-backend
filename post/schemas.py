from fastapi import Query
from pydantic import BaseModel
from typing import Optional

class PostListFilter(BaseModel):
    category_id: Optional[int] = Query(None, description="فیلتر بر اساس دسته‌بندی")
    author_id: Optional[int] = Query(None, description="فیلتر بر اساس نویسنده")
    search: Optional[str] = Query(None, description="جستجو در عنوان یا محتوا")
    ordering: Optional[str] = Query(
        "-create_time", description="مرتب‌سازی (مثلا: create_time یا -create_time)"
    )

class PostResponseSchema(BaseModel):
    id: int
    title: str
    description: str
    image: str
    category: str
    author: str
    create_time: str
