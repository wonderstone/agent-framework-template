### 1. Verdict: What Should the Template Absorb Next?
The template should absorb OpenSpace's **lineage tracking (FIX/DERIVED/CAPTURED)** and **metric-driven triggers** to build a structured "execution-to-candidate" pipeline. This effectively bridges the current execution gap by capturing runtime adaptations, while strictly relying on the existing, governance-heavy harvest loop to handle the actual promotion to canonical status. Direction C (with elements of D) is the most viable path forward.

### 2. Top 3 Findings

**Finding 1: Disconnected Execution Feedback Loop**
- **Category:** execution gap
- **Why it matters:** Currently, the governance-rich harvest loop starves. If an agent dynamically fixes a problem or invents a better approach during a task, that knowledge dies with the session. There is no structural bridge between a successful ad-hoc runtime adaptation and the candidate pipeline.
- **Smallest honest next step:** Introduce a standardized "execution delta" or "runtime receipt" artifact that agents emit after modifying a workflow, explicitly categorizing the change to feed directly into the `skill_candidate_packet`.

**Finding 2: Missing Host Integration / Invocation Surface**
- **Category:** missing runtime surface
- **Why it matters:** The template is heavily focused on what a skill *is* (governance, documentation, contracts) but lacks a standard for how it is *run*. Without a defined invocation boundary, metric-driven triggers (a core OpenSpace strength) have no execution data to act upon, rendering self-evolution impossible.
- **Smallest honest next step:** Draft a minimal runtime invocation protocol that standardizes how an agent loads a skill, records its usage, and reports its success/failure metrics back to the framework.

**Finding 3: Risk of Contextual Pollution in Canonical Skills**
- **Category:** over-automation risk
- **Why it matters:** Absorbing self-evolution mechanics risks creating a "raw transcript to canonical mutation" pipeline. If skills auto-update based on single execution traces, highly specific, contextual hacks will overwrite generalized, validated rules, destroying the integrity of the skill layer.
- **Smallest honest next step:** Enforce a hard architectural boundary where automated runtime captures *only* generate candidate packets in a pending directory. Maintain the strict requirement that promotion to a canonical asset requires discrete, validated authorization.

### 4. High-Value OpenSpace Idea
**Lineage Tracking (FIX/DERIVED/CAPTURED).** Adopting a formal taxonomy for *why* a skill candidate was generated is incredibly valuable. Knowing whether a candidate is an ad-hoc patch for a failing step (FIX), a specialized branch of an existing workflow (DERIVED), or a completely novel observation (CAPTURED) gives the governance layer the exact context it needs to make safe promotion decisions. 

### 5. OpenSpace Idea to Resist or Constrain
**Unsupervised Auto-Merging of Skill Updates.** The template must actively resist any OpenSpace mechanism that allows an agent or runtime loop to autonomously rewrite or merge updates directly into a canonical, promoted skill document. The framework must treat runtime adaptations purely as *proposals*, preserving the strict boundary between execution context and canonical truth.

### 6. Final Recommendation
**continue-discussion** 
*(Narrow the next round specifically to defining the schema for the "runtime receipt/delta" and how the FIX/DERIVED/CAPTURED lineage tags will be injected into the existing `skill_candidate_packet.template.md` before freezing a plan).*
