from __future__ import annotations

from src.task_tracker import render_demo_output


def test_render_demo_output_includes_priority_labels() -> None:
    output = render_demo_output()

    assert "[high]" in output
    assert "bootstrap repository" in output
