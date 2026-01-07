import pytest
from unittest.mock import MagicMock, patch
import os
from gh_wrapper.features.feature_tracer import FeatureTracer
from gh_wrapper.core.executor import GHExecutor

def test_trace_code_with_branches(mock_executor):
    executor, mock_run = mock_executor
    mock_run.reset_mock()
    mock_run.return_value.stdout = '[{"path": "test.py", "repository": {"full_name": "org/repo"}}]'
    
    tracer = FeatureTracer(executor)
    
    with patch.dict(os.environ, {"GH_ORG": "my-org"}):
        results = tracer.trace_code("bug", branches=["main", "dev"], limit=5)
        
    assert len(results) == 2 # 1 result per branch iteration
    assert results[0]['_scanned_branch'] == 'main'
    assert results[1]['_scanned_branch'] == 'dev'
    
    # Verify calls
    assert mock_run.call_count == 2
    args, _ = mock_run.call_args_list[0]
    cmd = args[0]
    assert 'gh' in cmd
    assert 'search' in cmd
    assert 'code' in cmd
    assert '--owner' in cmd
    assert 'my-org' in cmd
