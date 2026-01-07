import subprocess
import json
import os
from typing import List, Optional, Dict, Any, Union
from .exceptions import GHCommandError, GHNotInstalledError
from .cache import ResponseCache

class GHExecutor:
    """Enhanced executor for GitHub CLI commands with caching"""
    
    def __init__(
        self, 
        repo: Optional[str] = None,
        use_cache: bool = False,
        cache_ttl: int = 300  # 5 minutes
    ):
        self.repo = repo
        self.cache = ResponseCache(ttl=cache_ttl) if use_cache else None
        self._verify_gh_installed()
    
    def _verify_gh_installed(self):
        """Check if gh CLI is installed"""
        try:
            subprocess.run(
                ['gh', '--version'], 
                capture_output=True, 
                check=True,
                timeout=5
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise GHNotInstalledError(
                "GitHub CLI not installed. Install from: https://cli.github.com"
            )
        except subprocess.TimeoutExpired:
            raise GHCommandError("GitHub CLI command timed out")
    
    def execute(
        self, 
        command: List[str], 
        parse_json: bool = False,
        timeout: int = 30
    ) -> Union[str, Dict[str, Any], List[Any]]:
        """Execute a gh command and return output"""
        
        # Build full command
        cmd = ['gh'] + command
        
        # Enterprise Pathing & Environment handling
        # Pull directly from system environment during execution
        gh_host = os.getenv('GH_HOST')
        gh_org = os.getenv('GH_ORG')
        
        # Only append --repo for non-api commands
        # api commands must handle repo path themselves
        if self.repo and command[0] != 'api' and '--repo' not in command:
            repo_path = self.repo
            # Automatic formatting: prepend host/org if missing
            if '/' not in repo_path:
                parts = []
                if gh_host:
                    parts.append(gh_host)
                if gh_org:
                    parts.append(gh_org)
                parts.append(repo_path)
                
                # Join with forward slash if we have prefix parts
                if len(parts) > 1:
                    repo_path = "/".join(parts)
            
            cmd.extend(['--repo', repo_path])
        
        # Check cache
        cache_key = ' '.join(cmd)
        if self.cache:
            cached = self.cache.get(cache_key)
            if cached is not None:
                return cached
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                timeout=timeout,
                encoding='utf-8',
                errors='replace'
            )
            
            output = result.stdout.strip()
            
            # Parse JSON if requested
            if parse_json:
                try:
                    output = json.loads(output)
                except json.JSONDecodeError as e:
                    if not output:
                        return {{}}
                    raise GHCommandError(f"Failed to parse JSON: {e}\nOutput: {output[:100]}...")
            
            # Cache result
            if self.cache:
                self.cache.set(cache_key, output)
            
            return output
            
        except subprocess.CalledProcessError as e:
            raise GHCommandError(
                f"Command failed: {' '.join(cmd)}\n"
                f"Error: {e.stderr}"
            )
        except subprocess.TimeoutExpired:
            raise GHCommandError(
                f"Command timed out after {timeout}s: {' '.join(cmd)}"
            )
