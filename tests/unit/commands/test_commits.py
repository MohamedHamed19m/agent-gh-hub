import pytest
import json
from gh_wrapper.commands.commits import CommitsManager
from gh_wrapper.core.exceptions import GHCommandError

def test_list_commits(mock_executor, sample_commit_response):
    executor, mock_run = mock_executor
    # reset mock to ignore init calls
    mock_run.reset_mock()
    
    mock_run.return_value.stdout = json.dumps([sample_commit_response])
    
    manager = CommitsManager(executor)
    commits = manager.list_commits(branch="main", limit=5)
    
    assert len(commits) > 0
    assert commits[0]["sha"] == "abc123456789"
    
    # Verify arguments
    args, _ = mock_run.call_args
    # args[0] is the command list
    cmd = args[0]
    assert cmd[0] == 'gh'
    assert 'api' in cmd
    # We expect repos/test/repo/commits because executor.repo is set
    assert any('repos/test/repo/commits' in str(arg) for arg in cmd)

def test_search_commits(mock_executor):
    executor, mock_run = mock_executor
    mock_run.reset_mock()
    
    mock_run.return_value.stdout = json.dumps({"items": [{"sha": "search_result"}]})
    
    manager = CommitsManager(executor)
    results = manager.search_commits("bugfix")
    
    assert len(results) == 1
    assert results[0]["sha"] == "search_result"
