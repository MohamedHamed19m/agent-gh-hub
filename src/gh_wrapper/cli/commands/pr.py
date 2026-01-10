"""
Handler for the 'review-pr' command.
Agent B: Implementation of Markdown and Rich output.
"""

import sys

from rich.console import Console
from rich.markdown import Markdown

from gh_wrapper.commands.pull_requests import PRManager
from gh_wrapper.core.executor import GHExecutor
from gh_wrapper.features.pr_review_analyzer import PrReviewAnalyzer
from gh_wrapper.models.pr_review import PrReviewInput


def handle_review(repo: str, pr_id: int, readable: bool = False) -> None:
    """
    Execute PR review and format output.
    """
    executor = GHExecutor(repo=repo)
    pr_manager = PRManager(executor)
    analyzer = PrReviewAnalyzer(pr_manager)

    pr_input = PrReviewInput(repo_name=repo, pr_id=pr_id)

    try:
        report = analyzer.analyze_pr(pr_input)
        markdown_text = analyzer.format_as_markdown(report)

        if readable:
            console = Console()
            console.print(Markdown(markdown_text))
        else:
            # Default: Plain Markdown for agents
            sys.stdout.write(markdown_text)
            sys.stdout.write("\n")

    except Exception as e:
        sys.stderr.write(f"Error: {str(e)}\n")
        sys.exit(1)
