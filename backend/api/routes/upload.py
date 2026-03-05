from fastapi import APIRouter, UploadFile, File
import os
import uuid
import zipfile

from backend.config.settings import settings

router = APIRouter()

PROJECT_FOLDER = settings.PROJECT_STORAGE

@router.post("/upload")
async def upload_project(file: UploadFile = File(...)):

    project_id = str(uuid.uuid4())

    project_path = os.path.join(PROJECT_FOLDER, project_id)

    os.makedirs(project_path, exist_ok=True)

    zip_path = os.path.join(project_path, file.filename)

    with open(zip_path, "wb") as f:
        f.write(await file.read())

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(project_path)

    return {
        "project_id": project_id,
        "project_path": project_path
    }