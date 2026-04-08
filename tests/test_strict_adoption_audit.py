from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP_MODULE_PATH = REPO_ROOT / "scripts" / "bootstrap_adoption.py"
BOOTSTRAP_SPEC = importlib.util.spec_from_file_location("bootstrap_adoption_for_strict_audit", BOOTSTRAP_MODULE_PATH)
assert BOOTSTRAP_SPEC is not None
assert BOOTSTRAP_SPEC.loader is not None
BOOTSTRAP_MODULE = importlib.util.module_from_spec(BOOTSTRAP_SPEC)
sys.modules[BOOTSTRAP_SPEC.name] = BOOTSTRAP_MODULE
BOOTSTRAP_SPEC.loader.exec_module(BOOTSTRAP_MODULE)

bootstrap_repo = BOOTSTRAP_MODULE.bootstrap_repo


def test_strict_adoption_audit_reports_partially_adopted_without_review_evidence(tmp_path: Path) -> None:
    adopted_root = tmp_path / "adopted"
    bootstrap_repo(
        target_dir=adopted_root,
        project_name="Adopted Demo",
        profile="standard",
        project_type="cli-tool",
    )

    validation_evidence = adopted_root / "tmp" / "adoption_verification" / "validation.txt"
    validation_evidence.parent.mkdir(parents=True, exist_ok=True)
    validation_evidence.write_text("validator passed\n", encoding="utf-8")

    output_path = adopted_root / "tmp" / "adoption_verification" / "packet.md"
    result = subprocess.run(
        [
            sys.executable,
            str(adopted_root / "scripts" / "strict_adoption_audit.py"),
            "--root",
            str(adopted_root),
            "--validation-evidence",
            f"validator={validation_evidence.relative_to(adopted_root)}",
            "--output",
            str(output_path),
        ],
        cwd=adopted_root,
        check=True,
        capture_output=True,
        text=True,
    )

    assert result.stdout.strip() == str(output_path)
    rendered = output_path.read_text(encoding="utf-8")
    assert "- Adoption verdict: partially-adopted" in rendered
    assert "No independent review artifacts were supplied" in rendered


def test_strict_adoption_audit_rejects_non_passing_evidence(tmp_path: Path) -> None:
    adopted_root = tmp_path / "adopted"
    bootstrap_repo(
        target_dir=adopted_root,
        project_name="Adopted Demo",
        profile="standard",
        project_type="cli-tool",
    )

    validation_evidence = adopted_root / "tmp" / "adoption_verification" / "validation.txt"
    review_artifact = adopted_root / "tmp" / "adoption_verification" / "review.md"
    validation_evidence.parent.mkdir(parents=True, exist_ok=True)
    validation_evidence.write_text("validator failed\n", encoding="utf-8")
    review_artifact.write_text("Verdict: FAIL\n", encoding="utf-8")

    output_path = adopted_root / "tmp" / "adoption_verification" / "packet.md"
    subprocess.run(
        [
            sys.executable,
            str(adopted_root / "scripts" / "strict_adoption_audit.py"),
            "--root",
            str(adopted_root),
            "--validation-evidence",
            f"validator={validation_evidence.relative_to(adopted_root)}",
            "--review-artifact",
            f"cli-review={review_artifact.relative_to(adopted_root)}",
            "--output",
            str(output_path),
        ],
        cwd=adopted_root,
        check=True,
        capture_output=True,
        text=True,
    )

    rendered = output_path.read_text(encoding="utf-8")
    assert "- Adoption verdict: partially-adopted" in rendered
    assert "Validation evidence includes non-passing markers." in rendered


def test_strict_adoption_audit_reports_missing_mechanism_when_asset_removed(tmp_path: Path) -> None:
    adopted_root = tmp_path / "adopted"
    bootstrap_repo(
        target_dir=adopted_root,
        project_name="Adopted Demo",
        profile="standard",
        project_type="cli-tool",
    )

    (adopted_root / "scripts" / "developer_toolchain_probe.py").unlink()
    validation_evidence = adopted_root / "tmp" / "adoption_verification" / "validation.txt"
    review_artifact = adopted_root / "tmp" / "adoption_verification" / "review.md"
    validation_evidence.parent.mkdir(parents=True, exist_ok=True)
    validation_evidence.write_text("validator passed\n", encoding="utf-8")
    review_artifact.write_text("review passed\n", encoding="utf-8")

    output_path = adopted_root / "tmp" / "adoption_verification" / "packet.md"
    subprocess.run(
        [
            sys.executable,
            str(adopted_root / "scripts" / "strict_adoption_audit.py"),
            "--root",
            str(adopted_root),
            "--validation-evidence",
            f"validator={validation_evidence.relative_to(adopted_root)}",
            "--review-artifact",
            f"cli-review={review_artifact.relative_to(adopted_root)}",
            "--output",
            str(output_path),
        ],
        cwd=adopted_root,
        check=True,
        capture_output=True,
        text=True,
    )

    rendered = output_path.read_text(encoding="utf-8")
    assert "- Adoption verdict: partially-adopted" in rendered
    assert "developer-toolchain-probe | downgraded" in rendered
