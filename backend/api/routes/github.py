from fastapi import APIRouter
import git
import uuid
import os
from urllib.parse import quote

from backend.config.settings import settings

router = APIRouter()

PROJECT_FOLDER = settings.PROJECT_STORAGE

@router.post("/github")

def clone_repo(repo_url: str):

    project_id = str(uuid.uuid4())

    project_path = os.path.join(PROJECT_FOLDER, project_id)

    os.makedirs(project_path, exist_ok=True)

    effective_url = repo_url
    if settings.GITHUB_TOKEN and repo_url.startswith("https://github.com/"):
        token = quote(settings.GITHUB_TOKEN, safe="")
        effective_url = repo_url.replace("https://", f"https://{token}@", 1)

    git.Repo.clone_from(effective_url, project_path)

    return {
        "project_id": project_id,
        "project_path": project_path
    }