# Full Stack Workflow

Use this example when an adopted repository needs more than one runtime path.

## Workflow

1. Declare frontend and backend diagnostics separately.
2. Keep at least one concrete `Run` entry for each runtime that matters to day-to-day development.
3. Keep one `Health or smoke` entry close to the service layer and one cross-layer smoke or journey entry when the user flow spans both runtimes.
4. Keep one `Repro path` entry for the shortest stable user-visible journey.
5. Let the manifest enforce the required core while leaving richer helper surfaces advisory.

## Why Qualified Labels Matter

Multi-runtime repositories often fail when the adapter tries to collapse everything into one invented command.

Qualified labels avoid that by keeping the base surface stable while preserving the runtime context:

1. `Run (frontend)` still satisfies the `Run` contract
2. `Run (backend)` still satisfies the `Run` contract
3. the agent can choose the narrowest path that matches the touched surface and the required acceptance target