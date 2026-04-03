from __future__ import annotations

import importlib.util
import shutil
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "active_docs_audit.py"
SPEC = importlib.util.spec_from_file_location("active_docs_audit", MODULE_PATH)
assert SPEC is not None
assert SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

ActiveDocIssue = MODULE.ActiveDocIssue
audit_repo = MODULE.audit_repo


def test_active_docs_audit_passes_for_current_repository() -> None:
    issues = audit_repo(REPO_ROOT)

    assert issues == []


def test_active_docs_audit_reports_machine_local_absolute_path(tmp_path: Path) -> None:
    repo_copy = tmp_path / "repo"
    shutil.copytree(REPO_ROOT, repo_copy)

    readme = repo_copy / "README.md"
    readme.write_text(
        readme.read_text(encoding="utf-8") + "\nBroken path: /Users/tester/tmp/demo\n",
        encoding="utf-8",
    )

    issues = audit_repo(repo_copy)

    assert ActiveDocIssue(
        "nonportable-active-doc-path",
        "README.md: /Users/tester/tmp/demo",
    ) in issues


def test_active_docs_audit_reports_nonportable_python_entrypoint(tmp_path: Path) -> None:
    repo_copy = tmp_path / "repo"
    shutil.copytree(REPO_ROOT, repo_copy)

    readme = repo_copy / "README.md"
    readme.write_text(
        readme.read_text(encoding="utf-8").replace(
            "python3 scripts/bootstrap_adoption.py ../your-repo \\",
            "python scripts/bootstrap_adoption.py ../your-repo \\",
            1,
        ),
        encoding="utf-8",
    )

    issues = audit_repo(repo_copy)

    assert ActiveDocIssue(
        "nonportable-python-entrypoint",
        "README.md: python scripts/bootstrap_adoption.py",
    ) in issues


def test_active_docs_audit_reports_stale_active_doc_assertion(tmp_path: Path) -> None:
    repo_copy = tmp_path / "repo"
    shutil.copytree(REPO_ROOT, repo_copy)

    index_doc = repo_copy / "docs" / "INDEX.md"
    index_doc.write_text(
        index_doc.read_text(encoding="utf-8")
        + "\n## Project (create these for your project)\n| `ARCHITECTURE.md` | System architecture, module map, and service boundaries |\n",
        encoding="utf-8",
    )

    issues = audit_repo(repo_copy)

    assert ActiveDocIssue(
        "stale-active-doc-assertion",
        "docs/INDEX.md: ## Project (create these for your project)",
    ) in issues