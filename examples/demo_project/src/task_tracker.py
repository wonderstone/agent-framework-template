from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Task:
    title: str
    priority: str = "medium"


def list_tasks() -> list[Task]:
    return [
        Task("bootstrap repository", "high"),
        Task("fill project context", "high"),
        Task("record audit handoff", "medium"),
    ]


def format_tasks(tasks: list[Task]) -> str:
    lines = [f"- [{task.priority}] {task.title}" for task in tasks]
    return "\n".join(lines)


def render_demo_output() -> str:
    return format_tasks(list_tasks())


if __name__ == "__main__":
    print(render_demo_output())
