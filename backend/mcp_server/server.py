from fastapi import FastAPI
from backend.mcp_server.tools.list_files import list_files
from backend.mcp_server.tools.read_file import read_file
from backend.mcp_server.tools.search_code import search_code
from backend.mcp_server.tools.project_summary import project_summary

app = FastAPI()

@app.get("/tools")
def get_tools():
    return {
        "tools": [
            "list_files",
            "read_file",
            "search_code",
            "project_summary"
        ]
    }

@app.post("/tool/list_files")
def tool_list_files(project_path: str):
    return list_files(project_path)

@app.post("/tool/read_file")
def tool_read_file(project_path: str, file_path: str):
    return read_file(project_path, file_path)

@app.post("/tool/search_code")
def tool_search_code(project_path: str, keyword: str):
    return search_code(project_path, keyword)

@app.post("/tool/project_summary")
def tool_project_summary(project_path: str):
    return project_summary(project_path)