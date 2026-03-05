import os

def search_code(project_path, keyword):

    results = []

    for root, dirs, files in os.walk(project_path):

        for file in files:

            path = os.path.join(root, file)

            try:
                with open(path, "r", encoding="utf-8") as f:

                    for i, line in enumerate(f):

                        if keyword.lower() in line.lower():

                            results.append({
                                "file": path,
                                "line": i + 1,
                                "content": line.strip()
                            })

            except:
                pass

    return {"results": results}