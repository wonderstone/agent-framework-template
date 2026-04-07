I’m pulling the discussion packet and the nearby skill/runtime docs so the recommendation is grounded in this template rather than generic pattern-matching.

The packet confirms the core tension: governance is already real, execution isn’t. I’m reading the SKILL and runtime docs now to separate what the template already has from what OpenSpace would actually add.

I’ve confirmed the template already has a real constitutional layer for skills. What’s missing is a runtime plane that can observe invocation, outcomes, and bounded candidate generation without pretending that telemetry can rewrite truth on its own.

I have enough to make the call. The template should not jump to “self-rewriting skills”; it should add an execution-side evidence plane that can produce bounded, lineage-bearing candidates against the already-strong constitutional skill contract.

Appended feedback to `tmp/discussion/skill_self_evolution_execution_gap_v1/discussion_packet.md`.

1. **Verdict: what should the template absorb next?**  
Absorb a **thin execution plane** for SKILL use: structured invocation receipts, outcome classes, metric-triggered candidate creation, host/runtime integration points, and lineage across **CAPTURED -> DERIVED -> FIX**. Do **not** absorb self-rewriting canonical skills.

2. **Top 3 findings**

**1. Missing execution substrate**  
- **category:** execution gap  
- **why it matters:** The template can govern mutations, but it cannot yet observe skill invocation, success/failure, operator override, or reuse patterns in a structured way. That makes self-evolution mostly theoretical.  
- **smallest honest next step:** Add a non-canonical `skill_invocation_receipt` artifact and use it as the runtime evidence source for candidate packets.

**2. Existing constitutional boundaries are the asset, not the problem**  
- **category:** governance strength  
- **why it matters:** The current contract already gets the hard part right: receipt anchoring, field-level authority, and a ban on transcript-to-canonical mutation. Copying OpenSpace too literally would weaken trust by letting weak evidence impersonate authority.  
- **smallest honest next step:** Keep `purpose`, `triggers`, and `governance` human-only, and explicitly define FIX/DERIVED/CAPTURED as evidence layers, not mutation authority.

**3. Metrics without runtime surface + lineage will drift into fake certainty**  
- **category:** over-automation risk  
- **why it matters:** Metric-driven triggers are useful only if they point to declared runtime evidence and preserve provenance. Otherwise “smart through use” becomes heuristic prompt churn.  
- **smallest honest next step:** Start with a tiny trigger set—repeated invocation failure, repeated manual correction, repeated successful reference use—and require each trigger to resolve to a lineage chain before review begins.

3. **One OpenSpace idea that is high-value for this template**  
The **FIX / DERIVED / CAPTURED split**. It gives runtime observations and agent-derived proposals a truthful home without pretending they are canonical skill truth.

4. **One OpenSpace idea that this template should resist or heavily constrain**  
Any path from **raw traces/transcripts directly to canonical skill mutation**. Especially for normative fields and guardrails, that should stay prohibited or extremely constrained.

5. **Final recommendation**  
**freeze-plan**

