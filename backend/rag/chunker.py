import os

def chunk_project(project_path):

    chunks = []

    for root, dirs, files in os.walk(project_path):

        for file in files:

            if file.endswith((".py",".js",".ts",".java",".cs",".cpp",".go")):

                path = os.path.join(root, file)

                try:
                    with open(path, "r", encoding="utf-8") as f:

                        content = f.read()

                        parts = content.split("\n\n")

                        for p in parts:
                            if len(p) > 50:
                                chunks.append(p)

                except:
                    pass

    return chunks