"""Runtime surface registry template.

Copy or render to `.github/runtime_surface_registry.py` and replace the example values.
"""

SURFACES = [
    {
        "name": "primary_user_path",
        "exposure": "active_default_user_path",
        "trigger_prefixes": ("src/", "app/"),
        "protected_source_roots": ("src/",),
        "banned_phrases": (
            "PLACEHOLDER_RESPONSE_MARKER",
            "MOCK_EXECUTION_MARKER",
        ),
        "focused_tests": (
            "python -m pytest tests/test_primary_user_path.py -q",
        ),
        "live_commands": (
            "./scripts/smoke.sh",
        ),
    },
    {
        "name": "candidate_service_path",
        "exposure": "candidate_incubator_service",
        "trigger_prefixes": ("services/incubator/",),
        "protected_source_roots": ("services/incubator/",),
        "banned_phrases": (
            "CANDIDATE_PLACEHOLDER_MARKER",
        ),
        "focused_tests": (
            "python -m pytest tests/test_candidate_service.py -q",
        ),
        "live_commands": (),
    },
]