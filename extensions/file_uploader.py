import shutil
from pathlib import Path
from fastapi import UploadFile

def save_upload_file(upload_file: UploadFile, upload_dir: str = "uploads") -> str:

    Path(upload_dir).mkdir(parents=True, exist_ok=True) 
    file_path = Path(upload_dir) / upload_file.filename
    
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    
    return str(file_path)  
