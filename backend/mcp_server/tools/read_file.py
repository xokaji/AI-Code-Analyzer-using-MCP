import os

def read_file(project_path, file_path):
    full_path = os.path.join(project_path, file_path)

    if not os.path.exists(full_path):
        return {"error": "File not found"}

    with open(full_path, "r", encoding="utf-8") as f:
        content = f.read()

    return {"content": content}