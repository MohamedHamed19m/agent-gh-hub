from unittest.mock import patch

import pytest

from gh_wrapper.features.feature_tracer import FeatureTracer
from gh_wrapper.models.trace import MultiRepoFeatureTrace


@pytest.fixture
def tracer() -> FeatureTracer:
    return FeatureTracer()


def test_trace_feature_basic(tracer: FeatureTracer) -> None:
    # Mocking managers
    with (
        patch("gh_wrapper.features.feature_tracer.FileManager") as mock_file_class,
        patch(
            "gh_wrapper.features.feature_tracer.CommitsManager"
        ) as mock_commits_class,
        patch("gh_wrapper.features.feature_tracer.PRManager") as mock_pr_class,
    ):
        mock_file = mock_file_class.return_value
        mock_commits = mock_commits_class.return_value
        mock_pr = mock_pr_class.return_value

        mock_file.search_in_files.return_value = [
            {"path": "README.md", "snippet": "secure boot"}
        ]
        mock_commits.get_commits_for_analysis.return_value = [
            {
                "sha": "sha1",
                "commit": {
                    "message": "feat: secure boot",
                    "author": {
                        "name": "user1",
                        "email": "u1@e.com",
                        "date": "2023-01-01",
                    },
                },
                "parents": [],
            }
        ]
        mock_pr.list_prs.return_value = [
            {
                "number": 1,
                "title": "Implement secure boot",
                "author": {"login": "user1"},
                "createdAt": "2023-01-01",
                "labels": [],
                "draft": False,
            }
        ]

        report = tracer.trace_feature(
            keyword="secure boot",
            repos=["org/repo1"],
            branches=["main"],
            search_files=True,
            search_commits=True,
            search_prs=True,
        )

        assert isinstance(report, MultiRepoFeatureTrace)
        assert report.keyword == "secure boot"
        assert "org/repo1" in report.traces

        trace = report.traces["org/repo1"]
        assert len(trace.file_matches) == 1
        assert len(trace.commit_matches) == 1
        assert len(trace.pr_matches) == 1
        assert trace.commit_matches[0].sha == "sha1"


def test_trace_feature_toggles(tracer: FeatureTracer) -> None:
    with (
        patch("gh_wrapper.features.feature_tracer.FileManager") as mock_file_class,
        patch(
            "gh_wrapper.features.feature_tracer.CommitsManager"
        ) as mock_commits_class,
        patch("gh_wrapper.features.feature_tracer.PRManager") as mock_pr_class,
    ):
        report = tracer.trace_feature(
            keyword="test",
            repos=["org/repo1"],
            search_files=False,
            search_commits=False,
            search_prs=False,
        )

        trace = report.traces["org/repo1"]
        assert len(trace.file_matches) == 0
        assert len(trace.commit_matches) == 0
        assert len(trace.pr_matches) == 0

        # Verify no calls to managers
        assert mock_file_class.return_value.search_in_files.call_count == 0
        assert mock_commits_class.return_value.get_commits_for_analysis.call_count == 0
        assert mock_pr_class.return_value.list_prs.call_count == 0
