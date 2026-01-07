from typing import List, Dict, Optional
from ..core.executor import GHExecutor

class CommitsManager:
    def __init__(self, executor: GHExecutor):
        self.executor = executor

    def list_commits(self, branch: str = "main", limit: int = 10, path: Optional[str] = None) -> List[Dict]:
        """List commits from a branch, optionally filtering by path"""
        
        # Use :owner/:repo placeholders which gh CLI resolves if local, 
        # or use executor.repo if explicit
        if self.executor.repo:
            api_path = f"repos/{self.executor.repo}/commits"
        else:
            api_path = "repos/:owner/:repo/commits"

        params = [
            'api',
            api_path,
            '-F', f'sha={branch}',
            '-F', f'per_page={limit}'
        ]
        
        if path:
            params.extend(['-F', f'path={path}'])

        return self.executor.execute(params, parse_json=True)

    def search_commits(self, query: str, limit: int = 10) -> List[Dict]:
        """Search commits (using search api)"""
        q = f"{query}"
        if self.executor.repo:
            q += f" repo:{self.executor.repo}"
            
        params = [
            'api',
            'search/commits',
            '-F', f'q={q}',
            '-F', f'per_page={limit}'
        ]
        result = self.executor.execute(params, parse_json=True)
        return result.get('items', [])
