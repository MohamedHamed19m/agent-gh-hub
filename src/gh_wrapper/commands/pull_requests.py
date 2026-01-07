from typing import List, Dict
from ..core.executor import GHExecutor

class PRManager:
    def __init__(self, executor: GHExecutor):
        self.executor = executor

    def list_prs(self, state: str = "open", limit: int = 10) -> List[Dict]:
        """List pull requests"""
        cmd = [
            'pr', 'list',
            '--state', state,
            '--limit', str(limit),
            '--json', 'number,title,url,author,createdAt,state,headRefName,baseRefName'
        ]
        return self.executor.execute(cmd, parse_json=True)

    def get_pr_content(self, number: int) -> Dict:
        """Get PR details"""
        cmd = [
            'pr', 'view', str(number),
            '--json', 'number,title,body,comments,reviews,files'
        ]
        return self.executor.execute(cmd, parse_json=True)
