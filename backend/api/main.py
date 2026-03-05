from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes.analyze import router
from backend.api.routes.upload import router as upload_router
from backend.api.routes.github import router as github_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(upload_router)
app.include_router(github_router)