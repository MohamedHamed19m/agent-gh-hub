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

        params = ["api", api_path, "-F", f"ref={ref}"]

        try:
            data = self.executor.execute(params, parse_json=True)
        except GHCommandError:
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
            except Exception:
                return str(data["content"])  # Return raw if decode fails?
        return ""

    def list_files(self, path: str = "", ref: str = "main") -> List[Dict]:
        """List files in directory"""
        if self.executor.repo:
            api_path = f"repos/{self.executor.repo}/contents/{path}"
        else:
            api_path = f"repos/:owner/:repo/contents/{path}"

        params = ["api", api_path, "-F", f"ref={ref}"]

        result = self.executor.execute(params, parse_json=True)
        if isinstance(result, list):
            return result
        return []  # If it's a file, it returns dict, or empty
