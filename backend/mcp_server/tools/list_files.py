import os

def list_files(project_path):
    files = []

    for root, dirs, filenames in os.walk(project_path):
        for f in filenames:
            files.append(os.path.join(root, f))

    return {"files": files}