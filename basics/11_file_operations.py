import os
from pathlib import Path
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles

CURRENT_PATH = Path.cwd()
app = FastAPI()

# 1 - make sure upload folder exists
UPLOAD_DIR_NAME = 'uploads'
upload_dir = CURRENT_PATH / UPLOAD_DIR_NAME
upload_dir.mkdir(exist_ok=True)

# 2 - static_files
app.mount('/files', StaticFiles(directory=UPLOAD_DIR_NAME), name='files')

# 3 - upload file API
@app.post('/upload')
def upload_file(file: UploadFile=File(...)):
    filename = file.filename
    if not filename:
        raise HTTPException(
            status_code=400,
            detail='File not selected.'
        )
    
    file_path = os.path.join(UPLOAD_DIR_NAME, filename)
    with open(file_path, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
        return {
            'message': 'File uploaded successfully.',
            'filename': filename,
            'file_url': f'http://127.0.0.1/8000/{filename}'
        }
    
# 4 - download file API
@app.get('/files/{filename}')
def get_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR_NAME, filename)
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail='File not found.'
        )
    return {
        'file_url': f'http://127.0.0.1/8000/{filename}'
    }

# 5 - 
@app.get('/')
def home():
    return {
        'message': 'File upload API running.'
    }

