@echo off
SETLOCAL EnableDelayedExpansion

echo 🌳 Creating multi-agent worktree environment...

:: Create hidden directory for worktrees
if not exist ".trees" (
    mkdir .trees
)

:: Prevent Git from tracking worktree metadata
:: Checks if .trees/ is already in .gitignore
findstr /x ".trees/" .gitignore >nul 2>&1
if %errorlevel% neq 0 (
    echo .trees/ >> .gitignore
    git add .gitignore
    git commit -m "chore: ignore worktree directory"
)

:: Create isolated worktrees with dedicated branches
git worktree add .trees/agent_a -b feat/agent-a
git worktree add .trees/agent_b -b feat/agent-b

echo.
echo ✅ Worktrees created successfully!
echo.
echo 📁 Directory structure:
echo   .trees/agent_a/ - branch: feat/agent-a
echo   .trees/agent_b/ - branch: feat/agent-b
echo.
echo 🚀 Next steps:
echo   1. Run the Lead Agent prompt to create the plan
echo   2. Open CMD A: cd .trees\agent_a
echo   3. Open CMD B: cd .trees\agent_b
echo   4. Start both agents with their Worker Agent prompts

pause