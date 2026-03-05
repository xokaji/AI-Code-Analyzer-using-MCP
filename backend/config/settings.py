import os
from pathlib import Path

from dotenv import load_dotenv


_REPO_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(dotenv_path=_REPO_ROOT / ".env")

class Settings:
    
    MCP_SERVER_PORT = int(os.getenv("MCP_SERVER_PORT", 9000))

    MCP_SERVER_URL = os.getenv("MCP_SERVER_URL")

    BACKEND_PORT = int(os.getenv("BACKEND_PORT", 8000))

    VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "chroma")

    PROJECT_STORAGE = os.getenv("PROJECT_STORAGE", "data/projects")

    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

settings = Settings()