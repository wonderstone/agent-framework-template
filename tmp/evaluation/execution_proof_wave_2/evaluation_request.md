# Independent Evaluation Request

- Generated at: 2026-04-08T02:44:42.390938+00:00
- Task ID: execution_proof_wave_2
- Generator: implementer
- Evaluator: architect-review
- Review Scope: Wave 2 execution-proof rollout

## Goal

Confirm the Wave 2 execution-proof rollout is coherent across bootstrap, manifest, validator, tests, and state surfaces.

## UAC Focus

- [x] standard/full adopters inherit the Wave 2 runner, evaluation, and executor-review assets\n- [x] strict-adoption and toolchain proof surfaces stay semantically honest\n- [x] validator, tests, and smoke all pass

## Evidence To Review

- python3 scripts/validate_template.py\n- python3 -m pytest tests/ -q\n- python3 scripts/bootstrap_adoption.py "/var/folders/_j/lwz4tx1x5bs8rg99tcmb2mpr0000gn/T//agent-framework-template-smoke" --project-name "Smoke" --profile standard --project-type cli-tool --dry-run

## Allowed Files

- scripts/bootstrap_adoption.py\n- scripts/validate_template.py\n- scripts/strict_adoption_audit.py\n- scripts/developer_toolchain_probe.py\n- scripts/developer_toolchain_runner.py\n- scripts/evaluation_pipeline.py\n- scripts/review_dispatch.py\n- tests/\n- docs/\n- templates/\n- examples/full_stack_project/.github/

## Do Not Touch

- docs/archive/\n- unrelated worktree paths outside the Wave 2 rollout

## Verdict Contract

- Allowed verdicts: PASS, CONDITIONAL, FAIL
- Gap check: answer what the user would notice that generator-side tests might not catch
