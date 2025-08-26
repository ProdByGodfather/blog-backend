import os

from dotenv import load_dotenv

from abarorm import SQLiteModel
from abarorm.fields import sqlite

load_dotenv()

# Initialize FastAPI app
db_conf = {
    'db_name': os.getenv('DB_NAME')
}

class BaseModel(SQLiteModel):
    field = sqlite.CharField(max_length=100)
    class Meta:
        db_config = db_conf