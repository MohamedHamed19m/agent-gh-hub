from gh_wrapper.commands.commits import CommitsManager
from gh_wrapper.commands.files import FileManager
from gh_wrapper.core.executor import GHExecutor
from gh_wrapper.features.repo_context import RepoContextAnalyzer
from gh_wrapper.features.user_tracer import UserTracer


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
            print(f" -#{pr.get('number')}: {pr.get('title')}")
    else:
        print(" No open pull requests found.")

    readme_snippet = context.get("readme_snippet", "")
    print("\nREADME Snippet:\n")
    print(readme_snippet)


def get_commit_details_from_repo(repo_name: str, sha: str) -> None:
    executor = GHExecutor(repo=repo_name, use_cache=True)
    commits_manager = CommitsManager(executor)

    print(f"Fetching details for commit {sha} in {repo_name}...")
    commit_details = commits_manager.get_commit_details(sha)

    if commit_details:
        commit_info = commit_details.get("commit", {})
        author_info = commit_info.get("author", {})
        print("Commit Details:")
        print(f"SHA: {commit_details.get('sha')}")
        print(f"Author: {author_info.get('name')}")
        print(f"Date: {author_info.get('date')}")
        print(f"Message: {commit_info.get('message')}")

        files = commit_details.get("files", [])
        for file in files:
            additions = file.get("additions")
            deletions = file.get("deletions")
            filename = file.get("filename")
            print(f" - {filename}: +{additions} -{deletions}")
            if file.get("patch"):
                print(f"   Patch:\n{file.get('patch')}\n")
    else:
        print(f"No details found for commit {sha}.")


def trace_user_activity(username: str, repo_name: str, limit: int = 10) -> None:
    try:
        executor = GHExecutor(repo=repo_name, use_cache=True)
        user_tracer = UserTracer(executor)
        recent_work = user_tracer.trace_recent_work(username, repo_name, limit)

        print(
            f"\nRecent work traced for user '{username}' in repository '{repo_name}':"
        )

        if recent_work:
            for commit in recent_work:
                prefix = "" if commit.get("priority") else " "
                display_date = (
                    commit.get("date", "")[:10]
                    if commit.get("date")
                    else "unknown date"
                )
                sha = commit.get("sha")
                msg = commit.get("message")
                short_name = commit.get("short_name")
                branch = commit.get("branch")
                print(
                    f"{prefix} - [{sha}] {msg} by {short_name} "
                    f"on {display_date} (branch: {branch})"
                )
        else:
            print(
                f"No recent work found for user '{username}' "
                f"in repository '{repo_name}'."
            )
    except Exception as e:
        print(f"Error tracing user activity: {e}")


if __name__ == "__main__":
    repo_name = "MohamedHamed19m/agent-gh-hub"
    read_repo_content(repo_name)
    # read_specific_file(repo_name, "pyproject.toml")
    # get_commit_details_from_repo(repo_name, "main")
    # trace_user_activity("MohamedHamed19m", repo_name, limit=10)
