from abarorm.fields import sqlite as fields

from config.db import BaseModel
from account.models import User


class Category(BaseModel):
    title = fields.CharField(max_length=200)

class Post(BaseModel):
    title = fields.CharField(max_length=200)
    description = fields.TextField()
    image = fields.CharField(max_length=500)
    create_time = fields.DateTimeField(auto_now_add=True)
    category = fields.ForeignKey(Category, on_delete='SETNULL')
    author = fields.ForeignKey(User, on_delete='CASCADE')
    