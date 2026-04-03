# Full Stack Reference Project

This example is a richer reference repo for repositories that need a multi-runtime `Developer Toolchain` shape.

It is intentionally lightweight:

1. the files are small enough to inspect quickly
2. the focus is on framework surfaces, not application logic
3. the example demonstrates how frontend and backend runtime paths can coexist without collapsing into one fake run command

## What To Inspect

1. Open [.github/instructions/project-context.instructions.md](.github/instructions/project-context.instructions.md) to see qualified Developer Toolchain labels such as `Run (frontend)` and `Run (backend)`.
2. Open [.github/agent-framework-manifest.json](.github/agent-framework-manifest.json) to see the manifest-declared `required-core` Developer Toolchain contract.
3. Read [docs/runbooks/full-stack-workflow.md](docs/runbooks/full-stack-workflow.md) for the intended adoption flow.

## Why This Exists

The smaller [demo_project](../demo_project/) shows a single-runtime CLI adoption.

This example exists for the cases where a repository needs to describe:

1. frontend diagnostics separately from backend diagnostics
2. multiple run surfaces
3. a service-level smoke path and a full-stack repro path
4. one contract that still validates the shared required core