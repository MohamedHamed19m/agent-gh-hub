from gh_wrapper.commands.commits import CommitsManager
from gh_wrapper.core.executor import GHExecutor
from gh_wrapper.features.repo_analysis import RepoAnalyzer


def main() -> None:
    # 1. Initialize core components
    # Uses the current repository if none specified
    executor = GHExecutor()
    commits_manager = CommitsManager(executor)
    analyzer = RepoAnalyzer(commits_manager)

    print(f"Analyzing repository: {executor.repo or 'Local'}")

    # 2. Run analysis
    # We'll analyze 'main' and 'test-branch-fixture' if available
    branches = ["main", "test-branch-fixture"]

    print(f"Target branches: {', '.join(branches)}")
    print("Fetching data and generating insights (last 90 days)...")

    try:
        report = analyzer.analyze_commit_patterns(branches=branches, days_back=90)

        # 3. Display human-readable report
        markdown_report = analyzer.format_as_markdown(report)
        print("\n" + markdown_report)

    except Exception as e:
        print(f"Error during analysis: {e}")


if __name__ == "__main__":
    main()
