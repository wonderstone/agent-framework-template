Here is the evaluation of how the template should absorb Google's five SKILL design patterns.

### 1. Verdict: How should the template absorb the five patterns?
The template must explicitly reject the temptation to treat all five patterns as equal, conceptual "types of skills" in a documentation taxonomy. Instead, it should aggressively map the most structurally demanding patterns (Tool Wrapper, Pipeline, Reviewer) into concrete, shipped execution scaffolding and canonical contracts. The remaining patterns (Generator, Inversion) should be demoted to simple examples or entirely rejected to prevent the framework from devolving into abstract prompt engineering advice. Adopters need safe, runnable surfaces, not philosophical categories.

### 2. Top 3 Findings

**Finding 1: Tool Wrappers and Pipelines are the primary missing execution gaps.**
- **Category:** execution gap
- **Why it matters:** Adopters do not struggle with making an LLM generate text; they struggle with safely executing host commands and chaining those executions. If the framework leaves these as abstract concepts, adopters will reinvent insecure, brittle wrapper scripts.
- **Smallest honest next step:** Ship a concrete, validator-friendly Python execution scaffold (e.g., `tool_wrapper.template.py`) that strictly handles standard I/O, error catching, and timeout boundaries for wrapped host tools.

**Finding 2: Reviewers perfectly align with the existing validation paradigm but lack a unified contract.**
- **Category:** validator fit
- **Why it matters:** The framework already relies on `reviewer_roles/` for asynchronous quality enforcement. Formalizing the "Reviewer" pattern as a first-class canonical contract bridges the gap between static human review guidelines and active, agentic evaluation steps in CI.
- **Smallest honest next step:** Update `skill.template.md` and `reviewer_role_profile.template.md` to share a canonical interface for yielding pass/fail/escalate signals.

**Finding 3: Inversion threatens headless, CI-driven automation guarantees.**
- **Category:** governance fit
- **Why it matters:** The "Inversion" pattern (asking the user questions) is fundamentally interactive. Encouraging this pattern in an asynchronous, CI-heavy framework template risks introducing blocking runtime surfaces that break unattended workflows.
- **Smallest honest next step:** Explicitly document Inversion as an anti-pattern for core framework skills, advising adopters to push interactive requirements to the very edge of the host CLI instead.

### 4. Pattern Mapping Table

| Pattern | Mapping | Reason |
| :--- | :--- | :--- |
| **Tool Wrapper** | execution scaffold | Adopters require concrete, safe, and easily testable I/O boundaries to expose host capabilities. |
| **Reviewer** | canonical contract | Directly maps to the framework's need for strict, enforceable, and async quality boundaries. |
| **Pipeline** | execution scaffold | Orchestration requires real runnable scripts (like the existing pipeline scripts), not just Markdown advice. |
| **Generator** | example only | Generation is the default LLM behavior; over-scaffolding it leads to useless abstraction bloat. |
| **Inversion** | reject | Interactive prompts block headless/CI workflows and violate unattended execution guarantees. |

### 5. One thing this template must not do
This template **must not** invent a proprietary, abstract DSL (e.g., a complex YAML engine) to declare or wire together these patterns. It must stick to plain Python/shell execution scaffolding and Markdown governance contracts that remain readable and debuggable.

### 6. Final Recommendation
- **freeze-plan**
