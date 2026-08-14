# DIBO Derived Analysis Protocol

**Version: v0.1**

## Purpose

This protocol establishes the first reproducible method for analysis derived from DIBO primary observations. Its governing sequence is:

```text
Primary observation
  → Descriptive topology
  → Temporal description
  → Evaluative constructs
```

Describe first. Measure second. Evaluate last. Analysis must not begin by scoring institutions or labeling cases as dysfunctional.

## Relationship to DIBO v1.0.1

DIBO v1.0.1 defines the canonical primary-observation model. This protocol operates only on observations produced under that model and has the following compatibility baseline:

- DIBO v1.0.1;
- Git commit `420ca9330da8c60b1ce3516be50307694fff55e0`.

The canonical concepts remain Issue Lineage, Line, Episode, Transition, and Outcome. The canonical inputs remain [`../data/issues.csv`](../data/issues.csv), [`../data/episodes.csv`](../data/episodes.csv), and [`../data/transitions.csv`](../data/transitions.csv). This protocol changes neither their schemas nor the contributor-facing model.

Derived analysis must never overwrite or silently reinterpret canonical data.

## Analytical architecture

This protocol defines exactly three analytical layers.

### Layer 1 — Descriptive topology

**Question:** What structure is observable in the recorded Issue Lineage?

This layer derives reproducible structural descriptions from canonical Episodes and Transitions without normative judgment.

### Layer 2 — Temporal description

**Question:** How much observed time separates recorded institutional events?

This layer measures time in calendar days. It does not call an interval excessive, slow, delayed, or dysfunctional without a separate analytical rule.

### Layer 3 — Evaluative constructs

**Question:** Does an observed institutional pattern satisfy an explicitly defined substantive concept?

Potential constructs include Institutional Runaround, Decision Stall, Translation Loss, and Remedy Competition. They require additional evidence and explicit rules; they cannot be inferred mechanically from topology or elapsed time alone.

## Graph representation

For one Issue Lineage, define a directed graph:

```text
G = (V, E)
```

where `V` is the set of canonical Episodes for one `issue_id`, and `E` is the set of canonical Transitions for that same `issue_id`. An Episode node may carry canonical attributes including `episode_id`, `date`, `line`, and `institution`. A Transition edge may carry `transition_id`, `transition_date`, and `notes`.

The graph need not be a linear chain or complete. It represents only the observed, source-grounded institutional lineage recorded by DIBO. It does not claim to capture every real-world interaction, communication, meeting, causal influence, or institutional action. Absence of a node or edge is not proof that no activity occurred.

## Topology descriptors

The v0.1 core is deliberately small. All descriptors are computed within one `issue_id`.

### Counts

- `episode_count`: number of canonical Episodes.
- `transition_count`: number of canonical Transitions.
- Episode counts by Line: separate counts for `L`, `A`, and `J`.
- Transition counts by Line pair: derive `from_line` and `to_line` from the endpoint Episodes and count each of `L → L`, `L → A`, `L → J`, `A → L`, `A → A`, `A → J`, `J → L`, `J → A`, and `J → J` when present.

These counts are descriptions, not institutional performance measures.

### Edge descriptors

- `same_line = TRUE` when `from_line == to_line`; otherwise `FALSE`.
- `cross_line = TRUE` when `from_line != to_line`; otherwise `FALSE`.

Same-Line continuation is not inherently positive or negative. Cross-Line movement is not necessarily progress.

### Node descriptors

- `branch_node = TRUE` when a canonical Episode has `outdegree >= 2`; otherwise `FALSE`.
- `multiple_incoming = TRUE` when a canonical Episode has `indegree >= 2`; otherwise `FALSE`.
- A root has `indegree == 0`.
- A sink has `outdegree == 0`.

A branch means only that more than one recorded Transition leaves an Episode. At this descriptive layer, use the neutral term *multiple-incoming node*, not *convergence*. More than one root or sink is permitted and does not alone indicate methodological error.

### Connected components

An analysis may report the number of weakly connected components. A disconnected observed graph may reflect missing evidence or an intentionally bounded reconstruction. Analysts must not invent edges to force connectivity.

## Temporal measures

All date arithmetic uses calendar days.

### Edge latency

For each Transition:

```text
edge_latency_days = date(to_episode) - date(from_episode)
```

Use canonical Episode dates, not `transition_date` as an independent endpoint. Episodes on the same date produce `0`. A negative result is a data-integrity warning and must not be replaced silently by its absolute value.

### Observed lineage span

```text
lineage_span_days = latest canonical Episode date
                    - earliest canonical Episode date
```

This is the observed span of the canonical Episode record, not automatically resolution latency or time to remedy.

### Same-Line and cross-Line edge latency

Analyses may summarize `edge_latency_days` separately for same-Line and cross-Line Transitions. Longer same-Line intervals are not necessarily worse, and shorter cross-Line intervals are not necessarily better.

### Lineage age at an explicit cutoff

When the age of an open Issue Lineage is needed, the analysis must declare an `as_of_date` and record it with the run:

```text
lineage_age_days = as_of_date - start_date
```

The analyst's current system date must never be used silently.

### Time is not delay

A measured interval is not automatically a delay. Long elapsed time may reflect ordinary appeals, legally required procedure, evidence collection, implementation work, genuinely slow processing, unobserved activity, or other causes. Therefore, `edge_latency_days` and `lineage_span_days` are descriptive only and must not be called delay, stall, failure, or runaround without separate evidence and rules.

Resolution Latency is not operationalized in v0.1. The canonical model does not impose one universal resolution state. Any future method must define endpoints such as authoritative decision, remedy, implementation, system revision, or resolution for its particular analytical question.

## Interpretation boundaries

Topology describes structure; it does not evaluate institutional quality. None of the following alone establishes progress or dysfunction:

- high Episode or Transition counts;
- many cross-Line edges or same-Line continuation;
- branching or multiple incoming edges;
- multiple roots or sinks;
- long graph paths;
- long elapsed time.

At the deterministic layer, use neutral descriptions such as *branch node*, *multiple-incoming node*, *common later node*, and *parallel recorded paths*. Multiple incoming edges must not automatically be called convergence, and v0.1 defines no convergence score. Substantive convergence requires a later interpretive protocol.

A directed graph cycle is a strict graph-theoretic property. Institutional return or Line re-entry is not necessarily a directed cycle: a Line sequence such as `J → L → J` can occur while the Episode graph remains temporally acyclic. V0.1 does not equate these concepts or operationalize Open Cycle or Cycle Closure.

Evaluative constructs are not direct properties of the canonical graph. They may require additional source review, explicit derived coding, domain knowledge, and uncertainty handling. No evaluative construct may be inferred solely from the number of Transitions, institutions, or Lines; elapsed time; branching; or multiple incoming edges.

## Institutional Runaround

### Definition

Institutional Runaround is a pattern within a defined observed sequence in which the specific request, remedy, responsibility question, or explicitly scoped aspect being tracked is repeatedly redirected, reassigned, returned, or displaced among institutional actors while no actor provides a substantive disposition of that tracked matter, and the routing does not demonstrably move it through a necessary path toward an actor or process capable of authoritative decision, remedy, or implementation.

The central idea is movement without corresponding authoritative uptake or disposition. This is not reducible to a progress score.

### Evidence concepts

These concepts are reserved for future derived coding and must not be added to the canonical CSVs.

**Documented redirection:** source-grounded evidence that an institution directs, refers, or returns the issue elsewhere; declines substantive handling because another actor should handle it; or reassigns responsibility for the requested action. Thematic continuity alone is not documented redirection.

**Substantive disposition:** an authoritative institutional action that substantively addresses the issue presented, such as granting or denying a legal claim, enacting or rejecting a proposal, issuing an authoritative administrative determination, or creating or implementing a remedy. A negative substantive decision remains a disposition; an institution saying “no” is not by itself Runaround.

**Procedurally necessary routing:** movement required by an ordinary or legally structured process, such as ordinary judicial appeal, legislation followed by legally required implementation, or formally required review stages. Multiple institutions in necessary routing do not by themselves establish Runaround.

**Responsibility displacement:** source-grounded evidence that relevant actors repeatedly position substantive responsibility or authority elsewhere without accepting or reaching a disposition. This concept does not permit an inference of institutional bad faith.

### Classification rule

No numerical Runaround score is defined. A future assessment must use exactly `ESTABLISHED`, `NOT_ESTABLISHED`, or `INDETERMINATE`.

#### ESTABLISHED

Classify an observed sequence as `ESTABLISHED` only when all of the following are source-grounded:

1. A connected observed sequence contains at least two documented redirections or responsibility displacements among distinct institutional actors or units.
2. The relevant sequence contains no substantive disposition of the specific request, remedy, responsibility question, or explicitly scoped aspect being assessed.
3. Ordinary procedurally necessary routing toward authoritative consideration does not adequately explain the sequence.
4. At least one of these additional conditions holds:
   - the issue returns to a previously encountered actor or institutional location without an intervening substantive disposition; or
   - responsibility or authority is repeatedly displaced among actors such that no actor accepts or reaches substantive disposition.

#### NOT_ESTABLISHED

Use `NOT_ESTABLISHED` when the evidence is adequate for assessment and the required conditions are not met. Examples include ordinary necessary movement through several institutions, a substantive negative decision, movement leading to authoritative decision or implementation, or long duration without repeated responsibility displacement.

#### INDETERMINATE

Use `INDETERMINATE` when evidence is insufficient to determine whether a transfer was genuinely a redirection, a route was procedurally necessary, substantive responsibility was displaced, or a substantive disposition occurred. Missing evidence must not be converted into `ESTABLISHED`.

### Sequence-level scope

Runaround may characterize a particular observed sequence within an Issue Lineage; it need not characterize the whole lineage. Every future assessment must identify the specific request, remedy, responsibility question, or explicitly scoped aspect being tracked, as well as the start and end Episodes, included Episodes and Transitions, source evidence, and classification. V0.1 does not implement a storage format.

### Exclusions

No topology or time heuristic is sufficient. Prohibited rules include:

- `Transitions >= N → Runaround`;
- `Cross-Line movements >= N → Runaround`;
- `Lineage age >= N days → Runaround`;
- a Line pattern such as `A → J → L → A → Runaround`;
- branch present `→ Runaround`;
- return to a previous Line `→ Runaround`.

Nor are the following Runaround by themselves: a court declining a claim through an authoritative judgment; judicial appeal; referral required by statute; Diet committee consideration; budget authorization followed by implementation; competing bills; government development of an alternative remedy; partial remedy; branch structure; common-response structure; long duration; repeated reconsideration; or unresolved status.

### Distinctions from other constructs

Runaround concerns repeated displacement or routing of responsibility. A future Decision Stall construct would concern a lack of material institutional movement or disposition over time. An issue may stall without Runaround, experience Runaround without a long stall, experience both, or experience neither.

Latency is elapsed observed time; Runaround is an institutional routing pattern. High latency does not establish Runaround, low latency does not establish its absence, and no day threshold applies.

Multiple institutional proposals responding to the same problem are not inherently Runaround. Competing remedies may represent active institutional consideration and require a separate method.

### Uncertainty

The final Institutional Runaround classification has exactly three permitted values: `ESTABLISHED`, `NOT_ESTABLISHED`, and `INDETERMINATE`. `UNKNOWN` and *not observed* are not additional final classification states; they may be used only for individual evidence elements, derived coding fields, or unavailable observations.

Derived analysis must preserve uncertainty rather than force a binary inference. An absent Episode does not prove institutional inactivity; an absent Transition does not prove that no communication or influence occurred; and absent evidence of formal referral does not prove that no informal influence existed. DIBO reports what the recorded evidence supports.

## Reproducibility

Every future derived-analysis run or artifact should identify at minimum:

- canonical data version or Git commit/tag;
- Derived Analysis Protocol version;
- analysis code version or commit, when code exists;
- `as_of_date` when time-dependent measures are used;
- included Issue Lineage IDs;
- additional derived coding used;
- unresolved uncertainty.

V0.1 specifies these requirements but does not create a metadata schema.

## Separation from primary data

Derived analysis must never write calculated values into [`../data/issues.csv`](../data/issues.csv), [`../data/episodes.csv`](../data/episodes.csv), or [`../data/transitions.csv`](../data/transitions.csv). It must not silently alter or reinterpret primary observations.

If analysis reveals a factual error in canonical data, the correction must follow the normal DIBO correction process separately. Derived classifications remain outside the canonical contributor-facing fields.

## Deferred constructs

The following remain unresolved for later protocol versions and are not operationalized here:

- Resolution Latency;
- Referral-to-Uptake Latency;
- Decision Stall;
- Translation Loss;
- Remedy Competition;
- Remedy Reframing;
- Responsibility Vacuum;
- Judicial Re-entry classification;
- substantive Convergence classification;
- Open Cycle / Cycle Closure;
- global institutional performance scores.

## Status and limitations

DIBO Derived Analysis Protocol v0.1 is an initial methodological specification requiring further validation. It does not claim causal identification, complete institutional-process capture, validated performance measurement, proven reliability, established generalizability, or objective institutional quality scores.

The existing canonical Issue Lineages inform internal consistency checks only. They do not validate the framework, and this protocol publishes no case classifications, comparative metrics, or analytical results.
