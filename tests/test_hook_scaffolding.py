from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP_MODULE_PATH = REPO_ROOT / "scripts" / "bootstrap_adoption.py"
BOOTSTRAP_SPEC = importlib.util.spec_from_file_location("bootstrap_adoption_for_hooks", BOOTSTRAP_MODULE_PATH)
assert BOOTSTRAP_SPEC is not None
assert BOOTSTRAP_SPEC.loader is not None
BOOTSTRAP_MODULE = importlib.util.module_from_spec(BOOTSTRAP_SPEC)
sys.modules[BOOTSTRAP_SPEC.name] = BOOTSTRAP_MODULE
BOOTSTRAP_SPEC.loader.exec_module(BOOTSTRAP_MODULE)

bootstrap_repo = BOOTSTRAP_MODULE.bootstrap_repo


def _run(
    command: list[str],
    *,
    cwd: Path,
    check: bool = True,
    input_text: str | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        check=check,
        capture_output=True,
        text=True,
        input=input_text,
    )


def _init_repo(path: Path) -> None:
    _run(["git", "init"], cwd=path)
    _run(["git", "config", "user.name", "Test User"], cwd=path)
    _run(["git", "config", "user.email", "test@example.com"], cwd=path)


def _write_registry(path: Path) -> None:
    registry = path / ".github" / "runtime_surface_registry.py"
    registry.write_text(
        "SURFACES = [\n"
        "    {\n"
        "        'name': 'primary',\n"
        "        'exposure': 'active_default_user_path',\n"
        "        'trigger_prefixes': ('src/',),\n"
        "        'protected_source_roots': ('src/',),\n"
        "        'banned_phrases': ('PLACEHOLDER_RESPONSE_MARKER',),\n"
        "        'focused_tests': ('python -c \"raise SystemExit(0)\"',),\n"
        "        'live_commands': ('python -c \"raise SystemExit(0)\"',),\n"
        "    },\n"
        "]\n",
        encoding="utf-8",
    )


def _bootstrap_with_hooks(path: Path) -> None:
    bootstrap_repo(
        target_dir=path,
        project_name="Hook Demo",
        profile="minimal",
        project_type="cli-tool",
        capabilities=("closeout-audit", "runtime-guards", "git-hooks"),
    )
    _write_registry(path)
    _run(["bash", "scripts/install_git_hooks.sh"], cwd=path)


def test_install_git_hooks_sets_hooks_path(tmp_path: Path) -> None:
    _init_repo(tmp_path)
    _bootstrap_with_hooks(tmp_path)

    result = _run(["git", "config", "core.hooksPath"], cwd=tmp_path)

    assert result.stdout.strip() == ".githooks"


def test_pre_commit_hook_blocks_unanchored_closeout_claim(tmp_path: Path) -> None:
    _init_repo(tmp_path)
    _bootstrap_with_hooks(tmp_path)

    session_state = tmp_path / "session_state.md"
    session_state.write_text(session_state.read_text(encoding="utf-8") + "\ncompleted\n", encoding="utf-8")
    _run(["git", "add", "session_state.md"], cwd=tmp_path)

    result = _run(["bash", ".githooks/pre-commit"], cwd=tmp_path, check=False)

    assert result.returncode == 1
    assert "closeout truth audit failed" in result.stdout


def test_pre_push_hook_blocks_runtime_surface_regression(tmp_path: Path) -> None:
    _init_repo(tmp_path)
    _bootstrap_with_hooks(tmp_path)

    _run(["git", "add", "."], cwd=tmp_path)
    _run(["git", "commit", "-m", "baseline"], cwd=tmp_path)

    source = tmp_path / "src" / "handler.py"
    source.parent.mkdir(parents=True, exist_ok=True)
    source.write_text("PLACEHOLDER_RESPONSE_MARKER\n", encoding="utf-8")
    _run(["git", "add", "src/handler.py"], cwd=tmp_path)
    _run(["git", "commit", "--no-verify", "-m", "introduce regression"], cwd=tmp_path)
    head_sha = _run(["git", "rev-parse", "HEAD"], cwd=tmp_path).stdout.strip()

    result = _run(
        ["bash", ".githooks/pre-push"],
        cwd=tmp_path,
        check=False,
        input_text=f"refs/heads/main {head_sha} refs/heads/main 0000000000000000000000000000000000000000\n",
    )

    assert result.returncode == 1
    assert "runtime surface push-check findings" in result.stdout
    assert "banned phrase" in result.stdout


def test_pre_push_hook_requires_clean_worktree(tmp_path: Path) -> None:
    _init_repo(tmp_path)
    _bootstrap_with_hooks(tmp_path)

    source = tmp_path / "src" / "handler.py"
    source.parent.mkdir(parents=True, exist_ok=True)
    source.write_text("canonical output\n", encoding="utf-8")
    _run(["git", "add", "."], cwd=tmp_path)
    _run(["git", "commit", "-m", "baseline"], cwd=tmp_path)

    source.write_text("PLACEHOLDER_RESPONSE_MARKER\n", encoding="utf-8")
    head_sha = _run(["git", "rev-parse", "HEAD"], cwd=tmp_path).stdout.strip()

    result = _run(
        ["bash", ".githooks/pre-push"],
        cwd=tmp_path,
        check=False,
        input_text=f"refs/heads/main {head_sha} refs/heads/main 0000000000000000000000000000000000000000\n",
    )

    assert result.returncode == 1
    assert "requires a clean working tree" in result.stdout


def test_pre_push_hook_blocks_root_commit_runtime_regression(tmp_path: Path) -> None:
    _init_repo(tmp_path)
    _bootstrap_with_hooks(tmp_path)

    source = tmp_path / "src" / "handler.py"
    source.parent.mkdir(parents=True, exist_ok=True)
    source.write_text("PLACEHOLDER_RESPONSE_MARKER\n", encoding="utf-8")
    _run(["git", "add", "."], cwd=tmp_path)
    _run(["git", "commit", "--no-verify", "-m", "root regression"], cwd=tmp_path)
    head_sha = _run(["git", "rev-parse", "HEAD"], cwd=tmp_path).stdout.strip()

    result = _run(
        ["bash", ".githooks/pre-push"],
        cwd=tmp_path,
        check=False,
        input_text=f"refs/heads/main {head_sha} refs/heads/main 0000000000000000000000000000000000000000\n",
    )

    assert result.returncode == 1
    assert "banned phrase" in result.stdout


def test_pre_push_hook_blocks_untracked_runtime_surface_files(tmp_path: Path) -> None:
    _init_repo(tmp_path)
    _bootstrap_with_hooks(tmp_path)

    _run(["git", "add", "."], cwd=tmp_path)
    _run(["git", "commit", "-m", "baseline"], cwd=tmp_path)
    head_sha = _run(["git", "rev-parse", "HEAD"], cwd=tmp_path).stdout.strip()

    untracked = tmp_path / "src" / "untracked.py"
    untracked.parent.mkdir(parents=True, exist_ok=True)
    untracked.write_text("PLACEHOLDER_RESPONSE_MARKER\n", encoding="utf-8")

    result = _run(
        ["bash", ".githooks/pre-push"],
        cwd=tmp_path,
        check=False,
        input_text=f"refs/heads/main {head_sha} refs/heads/main 0000000000000000000000000000000000000000\n",
    )

    assert result.returncode == 1
    assert "requires a clean working tree" in result.stdout