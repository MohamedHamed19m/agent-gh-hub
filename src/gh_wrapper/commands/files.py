import base64
from typing import Dict, List

from ..core.exceptions import GHCommandError
from ..core.executor import GHExecutor


class FileManager:
    def __init__(self, executor: GHExecutor):
        self.executor = executor

    def get_file_content(self, path: str, ref: str = "main") -> str:
        """Get raw content of a file"""
        if self.executor.repo:
            api_path = f"repos/{self.executor.repo}/contents/{path}"
        else:
            api_path = f"repos/:owner/:repo/contents/{path}"

        # Strip trailing slash if path is empty (though usually it's a file path)
        api_path = api_path.rstrip("/")

        # Using query parameter because -F ref=xxx causes 404 in some cases
        params = ["api", f"{api_path}?ref={ref}"]

        try:
            data = self.executor.execute(params, parse_json=True)
        except GHCommandError as e:
            print(f"Error fetching file content: {e}")
            return ""  # Or raise?

        if (
            isinstance(data, dict)
            and "content" in data
            and data.get("encoding") == "base64"
        ):
            try:
                content = base64.b64decode(data["content"]).decode(
                    "utf-8", errors="replace"
                )
                return content
            except Exception as e:
                print(f"Error decoding file content: {e}")
                return str(data["content"])
        else:
            print(f"file {path} data is not as expected: {data}")
        return ""

    def list_files(self, path: str = "", ref: str = "main") -> List[Dict]:
        """List files in directory"""
        if self.executor.repo:
            api_path = f"repos/{self.executor.repo}/contents/{path}"
        else:
            api_path = f"repos/:owner/:repo/contents/{path}"

        # Strip trailing slash if path is empty
        api_path = api_path.rstrip("/")

        # Using query parameter because -F ref=xxx causes 404 for root
        # directory in some cases
        params = ["api", f"{api_path}?ref={ref}"]

        result = self.executor.execute(params, parse_json=True)
        if isinstance(result, list):
            return result
        return []  # If it's a file, it returns dict, or empty

    def search_in_files(self, query: str, limit: int = 50) -> List[Dict]:
        """Search code for a keyword using 'gh search code'"""
        cmd = [
            "search",
            "code",
            query,
            "--repo",
            self.executor.repo or "",
            "--limit",
            str(limit),
            "--json",
            "path,text_matches",
        ]
        result = self.executor.execute(cmd, parse_json=True)
        if isinstance(result, list):
            matches = []
            for item in result:
                snippet = None
                if item.get("text_matches"):
                    # Get the first match fragment
                    snippet = item["text_matches"][0].get("fragment")
                matches.append({"path": item.get("path"), "snippet": snippet})
            return matches
        return []
