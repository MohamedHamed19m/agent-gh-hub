import sys
import os

# Add src to path for demo purposes if not installed
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from gh_wrapper.core.executor import GHExecutor
from gh_wrapper.commands.commits import CommitsManager
from gh_wrapper.features.feature_tracer import FeatureTracer

def main():
    print("Initializing GitHub Wrapper Demo...")
    try:
        # You can change the repo to test different contexts
        executor = GHExecutor(repo="cli/cli") 
        print(f"Targeting repo: {executor.repo}")
    except Exception as e:
        print(f"Error initializing (check if gh is installed and auth): {e}")
        return

    print("\n--- Testing Commits Manager ---")
    commits_mgr = CommitsManager(executor)
    try:
        commits = commits_mgr.list_commits(limit=3)
        for c in commits:
            sha = c.get('sha', '??????')[:7]
            msg = c.get('commit', {}).get('message', 'No message').splitlines()[0]
            print(f"- {sha}: {msg}")
    except Exception as e:
        print(f"Failed to list commits: {e}")

    print("\n--- Testing Feature Tracer ---")
    tracer = FeatureTracer(executor)
    try:
        # Search for something common
        query = "command"
        print(f"Searching for code matching '{query}'...")
        results = tracer.trace_code(query, limit=3)
        print(f"Found {len(results)} code results")
        for item in results:
            print(f"- {item.get('name')} ({item.get('path')})")
    except Exception as e:
        print(f"Failed to trace feature: {e}")

if __name__ == "__main__":
    main()
