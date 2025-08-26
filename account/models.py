from abarorm.fields import sqlite

from config.db import BaseModel


class User(BaseModel):
    username = sqlite.CharField(unique=True, max_length=200)
    password = sqlite.CharField(max_length=500)
    first_name = sqlite.CharField(max_length=100)
    last_name = sqlite.CharField(max_length=100)
    email = sqlite.EmailField(max_length=200)
    image = sqlite.CharField(max_length=500, null=True)
    is_superuser = sqlite.BooleanField(default=False)
    