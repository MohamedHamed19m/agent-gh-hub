import json
import os
import subprocess
from typing import Any, Dict, List, Optional, Union, cast

from .cache import ResponseCache
from .exceptions import GHCommandError, GHNotInstalledError


class GHExecutor:
    """Enhanced executor for GitHub CLI commands with caching"""

    _gh_installed_cached: bool = False

    def __init__(
        self,
        repo: Optional[str] = None,
        use_cache: bool = False,
        cache_ttl: int = 300,  # 5 minutes
    ) -> None:
        self.repo = repo
        self.cache = ResponseCache(ttl=cache_ttl) if use_cache else None
        self._verify_gh_installed()

    def _verify_gh_installed(self) -> None:
        """Check if gh CLI is installed (with caching)"""
        if GHExecutor._gh_installed_cached:
            return

        try:
            subprocess.run(
                ["gh", "--version"], capture_output=True, check=True, timeout=15
            )
            GHExecutor._gh_installed_cached = True
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise GHNotInstalledError(
                "GitHub CLI not installed. Install from: https://cli.github.com"
            )
        except subprocess.TimeoutExpired:
            raise GHCommandError("GitHub CLI version check timed out")

    def execute(
        self, command: List[str], parse_json: bool = False, timeout: int = 60
    ) -> Union[str, Dict[str, Any], List[Any]]:
        """Execute a gh command and return output"""
        # Build full command
        cmd = ["gh"] + command

        # Enterprise Pathing & Environment handling
        # Pull directly from system environment during execution
        gh_host = os.getenv("GH_HOST")
        gh_org = os.getenv("GH_ORG")

        # Only append --repo for non-api commands
        # api commands must handle repo path themselves
        if self.repo and "--repo" not in command:
            if command[0] == "api":
                pass
            elif self.repo in command:
                pass
            else:
                repo_path = self.repo
                # Automatic formatting: prepend host/org if missing
                if "/" not in repo_path:
                    parts = []
                    if gh_host:
                        parts.append(gh_host)
                    if gh_org:
                        parts.append(gh_org)
                    parts.append(repo_path)

                    # Join with forward slash if we have prefix parts
                    if len(parts) > 1:
                        repo_path = "/".join(parts)

                cmd.extend(["--repo", repo_path])
        # if self.repo and command[0] != "api" and "--repo" not in command:
        #     repo_path = self.repo
        #     # Automatic formatting: prepend host/org if missing
        #     if "/" not in repo_path:
        #         parts = []
        #         if gh_host:
        #             parts.append(gh_host)
        #         if gh_org:
        #             parts.append(gh_org)
        #         parts.append(repo_path)

        #         # Join with forward slash if we have prefix parts
        #         if len(parts) > 1:
        #             repo_path = "/".join(parts)

        #     cmd.extend(["--repo", repo_path])

        # Check cache
        cache_key = " ".join(cmd)
        if self.cache:
            cached = self.cache.get(cache_key)
            if cached is not None:
                return cast(Union[str, Dict[str, Any], List[Any]], cached)

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                timeout=timeout,
                encoding="utf-8",
                errors="replace",
            )

            output = result.stdout.strip()

            # Parse JSON if requested
            if parse_json:
                try:
                    output_data = json.loads(output)
                    # Cache result
                    if self.cache:
                        self.cache.set(cache_key, output_data)
                    return cast(Union[str, Dict[str, Any], List[Any]], output_data)
                except json.JSONDecodeError as e:
                    if not output:
                        return {}
                    raise GHCommandError(
                        f"Failed to parse JSON: {e}\nOutput: {output[:100]}..."
                    )

            # Cache result
            if self.cache:
                self.cache.set(cache_key, output)

            return cast(Union[str, Dict[str, Any], List[Any]], output)

        except subprocess.CalledProcessError as e:
            raise GHCommandError(f"Command failed: {' '.join(cmd)}\nError: {e.stderr}")
        except subprocess.TimeoutExpired:
            raise GHCommandError(f"Command timed out after {timeout}s: {' '.join(cmd)}")
