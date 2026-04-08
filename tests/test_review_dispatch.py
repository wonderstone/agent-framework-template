from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP_MODULE_PATH = REPO_ROOT / "scripts" / "bootstrap_adoption.py"
BOOTSTRAP_SPEC = importlib.util.spec_from_file_location("bootstrap_adoption_for_review_dispatch", BOOTSTRAP_MODULE_PATH)
assert BOOTSTRAP_SPEC is not None
assert BOOTSTRAP_SPEC.loader is not None
BOOTSTRAP_MODULE = importlib.util.module_from_spec(BOOTSTRAP_SPEC)
sys.modules[BOOTSTRAP_SPEC.name] = BOOTSTRAP_MODULE
BOOTSTRAP_SPEC.loader.exec_module(BOOTSTRAP_MODULE)

bootstrap_repo = BOOTSTRAP_MODULE.bootstrap_repo


def _write_registry(registry_path: Path) -> None:
    registry_path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "executors": [
                    {
                        "name": "alpha",
                        "probe_command": f"{sys.executable} -c \"import sys; sys.exit(0)\"",
                        "review_command": f"{sys.executable} -c \"from pathlib import Path; print(Path(r'{'{prompt_file}'}').read_text(encoding='utf-8').strip())\"",
                    },
                    {
                        "name": "beta",
                        "probe_command": f"{sys.executable} -c \"import sys; sys.exit(1)\"",
                        "review_command": f"{sys.executable} -c \"print('should not run')\"",
                    },
                ],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def test_review_dispatch_probes_and_dispatches(tmp_path: Path) -> None:
    adopted_root = tmp_path / "adopted"
    bootstrap_repo(
        target_dir=adopted_root,
        project_name="Adopted Demo",
        profile="standard",
        project_type="cli-tool",
    )

    registry_path = adopted_root / ".github" / "local_executor_registry.json"
    _write_registry(registry_path)
    prompt_file = adopted_root / "tmp" / "review_prompt.txt"
    prompt_file.parent.mkdir(parents=True, exist_ok=True)
    prompt_file.write_text("review prompt", encoding="utf-8")

    script_path = adopted_root / "scripts" / "review_dispatch.py"
    probe = subprocess.run(
        [
            sys.executable,
            str(script_path),
            "--root",
            str(adopted_root),
            "--review-id",
            "review-1",
            "probe",
        ],
        cwd=adopted_root,
        check=True,
        capture_output=True,
        text=True,
    )

    dispatch = subprocess.run(
        [
            sys.executable,
            str(script_path),
            "--root",
            str(adopted_root),
            "--review-id",
            "review-2",
            "dispatch",
            "--prompt-file",
            str(prompt_file),
        ],
        cwd=adopted_root,
        check=True,
        capture_output=True,
        text=True,
    )

    probe_packet = Path(probe.stdout.strip())
    dispatch_packet = Path(dispatch.stdout.strip())
    assert "| alpha | available | skipped | none | none | Probe command succeeded. |" in probe_packet.read_text(encoding="utf-8")
    dispatch_text = dispatch_packet.read_text(encoding="utf-8")
    assert "| alpha | available | completed |" in dispatch_text
    assert "| beta | unavailable | unavailable | none | none |" in dispatch_text
    stdout_path = adopted_root / "tmp" / "executor_reviews" / "review-2" / "raw" / "alpha.stdout"
    assert stdout_path.read_text(encoding="utf-8").strip() == "review prompt"