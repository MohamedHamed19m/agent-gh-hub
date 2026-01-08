from gh_wrapper.core.executor import GHExecutor
from gh_wrapper.features.repo_context import RepoContextAnalyzer
from gh_wrapper.commands.files import FileManager


def read_specific_file(repo_name: str, file_path: str) -> None:
    executor = GHExecutor(repo=repo_name, use_cache=True)
    file_manager = FileManager(executor)
    
    print(f"Reading content of {file_path} from {repo_name}...")
    content = file_manager.get_file_content(file_path)
    print("--------------------------------------------------")
    print(content)
    print("--------------------------------------------------")


def read_repo_content(repo_name: str) -> None:
    executor = GHExecutor(repo=repo_name, use_cache=True)

    analyzer = RepoContextAnalyzer(executor)
    context = analyzer.analyze_current_context()

    print(f"Repository Context for {repo_name}")
    print("Target Directory:", context.get("target"))

    metadata = context.get("metadata", {})
    print("Default Branch:", metadata.get("default_branch"))
    print("Description:", metadata.get("description"))
    print("Latest Release:", metadata.get("latest_release"))

    active_branches = metadata.get("active_branches", [])
    print("Active Branches:", ", ".join(active_branches))
    if active_branches:
        for branch in active_branches:
            print(" -", branch)
    else:
        print(" No active branches found.")

    structure = context.get("structure", {})
    if structure:
        for i, item in enumerate(structure):
            if i >= 10:
                print(" ... (truncated)")
                break
            print(f" - {item.get('path')} ({item.get('type')})")
    else:
        print(" No file structure found.")
    
    activity = context.get("activity", {})
    recent_commits = activity.get("recent_commits", [])
    print("Recent Commits:")
    if recent_commits:
        for commit in recent_commits:
            print(f" - {commit.get('sha')}: {commit.get('message')}")
    else:
        print(" No recent commits found.")

    open_prs = activity.get("open_prs", [])
    if open_prs:
        print("Open Pull Requests:")
        for pr in open_prs:
            print(f" - #{pr.get('number')}: {pr.get('title')}")
    else:
        print(" No open pull requests found.")

    readme_snippet = context.get("readme_snippet", "")
    print("\nREADME Snippet:\n")
    print(readme_snippet)



if __name__ == "__main__":
    repo_name = "MohamedHamed19m/agent-gh-hub"
    read_repo_content(repo_name)
    read_specific_file(repo_name, "pyproject.toml")
  