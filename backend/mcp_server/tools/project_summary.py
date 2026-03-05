from .list_files import list_files

def project_summary(project_path):

    files = list_files(project_path)["files"]

    summary = {
        "total_files": len(files),
        "important_files": []
    }

    for f in files:

        if "main" in f or "app" in f or "index" in f:
            summary["important_files"].append(f)

    return summary