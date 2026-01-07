from typing import List, Dict
from ..core.executor import GHExecutor

class UserManager:
    def __init__(self, executor: GHExecutor):
        self.executor = executor

    def get_user_activity(self, username: str, limit: int = 10) -> List[Dict]:
        """Get public events for a user"""
        params = [
            'api',
            f'users/{username}/events',
            '-F', f'per_page={limit}'
        ]
        return self.executor.execute(params, parse_json=True)
        
    def get_user_commits(self, username: str, limit: int = 10) -> List[Dict]:
        """Search commits by user (global search or repo context if specified in executor?)
        search/commits is global unless repo: is in q.
        """
        q = f"author:{username}"
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
