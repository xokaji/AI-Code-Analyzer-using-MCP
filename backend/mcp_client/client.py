import requests

from backend.config.settings import settings

MCP_SERVER = settings.MCP_SERVER_URL or f"http://127.0.0.1:{settings.MCP_SERVER_PORT}"

class MCPClient:

    def list_files(self, project_path):

        r = requests.post(
            f"{MCP_SERVER}/tool/list_files",
            params={"project_path": project_path}
        )

        return r.json()

    def read_file(self, project_path, file_path):

        r = requests.post(
            f"{MCP_SERVER}/tool/read_file",
            params={
                "project_path": project_path,
                "file_path": file_path
            }
        )

        return r.json()

    def search_code(self, project_path, keyword):

        r = requests.post(
            f"{MCP_SERVER}/tool/search_code",
            params={
                "project_path": project_path,
                "keyword": keyword
            }
        )

        return r.json()

    def project_summary(self, project_path):

        r = requests.post(
            f"{MCP_SERVER}/tool/project_summary",
            params={"project_path": project_path}
        )

        return r.json()