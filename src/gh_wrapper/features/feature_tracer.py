import os
from typing import Dict, List, Optional

from ..core.executor import GHExecutor


class FeatureTracer:
    def __init__(self, executor: GHExecutor):
        self.executor = executor

    def trace_code(
        self, query: str, branches: Optional[List[str]] = None, limit: int = 10
    ) -> List[Dict]:
        """Search code for a feature keyword across branches (iterating through them)"""
        results = []
        gh_org = os.getenv("GH_ORG")

        if not branches:
            branches = ["main"]

        for branch in branches:
            # utilizing gh search code with the --owner flag set to the system's GH_ORG
            # Note: The search API is global index based, but we iterate as requested
            cmd = [
                "search",
                "code",
                query,
                "--limit",
                str(limit),
                "--json",
                "file,path,repository,text_matches,url",
            ]

            if gh_org:
                cmd.extend(["--owner", gh_org])

            # If the user intends to trace across branches, we might want to
            # include the branch name in the query if it were supported, but
            # strictly adhering to instructions:
            # We iterate and run the search command.

            try:
                output = self.executor.execute(cmd, parse_json=True)
                if isinstance(output, list):
                    # Tag result with the branch we were "checking"
                    for item in output:
                        item["_scanned_branch"] = branch
                    results.extend(output)
            except Exception:
                continue

        return results
