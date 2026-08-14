# DIBO Codebook

**Version: DIBO v1.0.1**

## General conventions

- Store primary observations only in the three canonical CSV files.
- Use stable identifiers that are never reassigned.
- Use `YYYY-MM-DD` when a complete date is supported. Do not invent precision.
- Use concise factual language.
- Prefer official primary-source URLs. One Episode may cite multiple official sources when they document the same institutional event.
- Leave an optional field empty rather than inferring an unsupported value.

This clarification preserves the five canonical concepts—Issue Lineage, Line, Episode, Transition, and Outcome—and the three existing CSV schemas. It adds no required contributor classification.

Suggested identifier forms are `DIBO-JP-0001` for an Issue Lineage, `DIBO-JP-0001-E001` for an Episode, and `DIBO-JP-0001-T001` for a Transition.

## `data/issues.csv`

One row represents one Issue Lineage.

| Field | Definition |
| --- | --- |
| `issue_id` | Stable Issue Lineage identifier, such as `DIBO-JP-0001`. |
| `title` | Canonical short issue title. |
| `country` | ISO-style country code, such as `JP`. |
| `issue_summary` | Concise description of the underlying public problem. |
| `requested_change` | Change, remedy, correction, or institutional action being sought. |
| `start_date` | Earliest date included in the registered lineage. |
| `current_status` | Short, stable factual status supported by the available record. Avoid routinely changing counts and transient political commentary. |
| `notes` | Optional scope, boundary, or uncertainty note. |

Canonical header:

```csv
issue_id,title,country,issue_summary,requested_change,start_date,current_status,notes
```

## `data/episodes.csv`

One row represents one substantively meaningful, dated, observable, source-grounded institutional event. This is the main observational table.

| Field | Definition |
| --- | --- |
| `episode_id` | Stable identifier for a separate institutional act recorded as an Episode. |
| `issue_id` | Parent Issue Lineage identifier. |
| `date` | Date of the observed event. |
| `line` | Exactly one of `L`, `A`, or `J`, assigned by the institutional process where the observable action occurred. |
| `institution` | Institution or institutional body involved. |
| `what_happened` | Concise factual description of the event. |
| `result_or_next_step` | Observable Outcome or next step. It may include a later automatic status change directly related to the Episode, but does not imply final resolution. |
| `source` | Traceable source, preferably one or more official primary-source URLs supporting the factual event. |

Canonical header:

```csv
episode_id,issue_id,date,line,institution,what_happened,result_or_next_step,source
```

Not every state change is an Episode. A new Episode normally requires an observable action or decision that materially changes the institutional state. Passage of time, an automatic status change, a restatement, an updated statistic, or a changed political expectation is not sufficient by itself.

Keep separate institutional acts as separate Episodes even if they occur on the same date, within the same institution, or reach similar conclusions. Materially different proposals also remain separate when they are separate institutional actions. Multiple documents may support one Episode when they document the same event; one document does not necessarily require its own Episode.

Prefer the smallest Episode set that preserves meaningful state changes and a reconstructable lineage. Intermediate steps may be omitted when they do not materially change institutional state and their omission does not break reconstructability. Do not compress distinct primary events merely to simplify the graph or reduce the source count.

## `data/transitions.csv`

One row represents a supported connection between two Episodes.

| Field | Definition |
| --- | --- |
| `transition_id` | Stable Transition identifier. |
| `issue_id` | Parent Issue Lineage identifier. |
| `from_episode` | Origin Episode identifier. |
| `to_episode` | Destination Episode identifier. |
| `transition_date` | Date of the transition when supported. |
| `notes` | Optional factual note about the connection or uncertainty; do not imply referral, transfer, or causation unless supported. |

Canonical header:

```csv
transition_id,issue_id,from_episode,to_episode,transition_date,notes
```

A Transition may be same-Line or cross-Line. Valid edges include `J → J`, `A → A`, and `L → L`; a Transition does not require an institutional handoff.

The graph may branch, follow parallel paths, or have multiple incoming edges to a later common response. Preserve distinct earlier Episodes and record separate incoming edges rather than aggregating them to make the graph appear to converge.

A later Episode may be connected as issue-level uptake when it clearly concerns the same Issue Lineage. Chronology and thematic continuity do not by themselves establish formal referral, legal or jurisdictional transfer, causation, or a single-cause relationship. State such relationships only when the evidence supports them.

Contributors do not need to classify transitions as referrals, returns, branches, convergence, merges, stalls, or cycles. Those patterns may be derived from the recorded edges.

## Lines

| Code | Meaning |
| --- | --- |
| `L` | Legislative process, including bill introduction, committee action, enactment, or parliamentary budget authorization |
| `A` | Executive or administrative process, including formal policy adoption, implementation, or appropriate government preparation/submission activity |
| `J` | Judicial process, including judgments and decisions |

Assign the Line according to the process where the observable action occurred, not according to a presumed cause, desired remedy, or eventual destination. Do not add subtypes.

## Outcome

Outcome is a canonical concept, but it is not a separate table in the initial scaffold. Record the observable result or next step in `episodes.csv` under `result_or_next_step`. An Outcome may describe continuation, enactment, implementation, partial operation, non-adoption, pending action, reversal, or unresolved status. It does not imply final resolution.

An automatic legal status change may be recorded in `result_or_next_step`, `current_status`, or date-stamped case documentation when no new institutional action occurred. A later observable action, such as an order fixing a commencement date, may qualify as a new Episode.

## Derived analysis

Derived variables belong under [`analysis/`](analysis/README.md). They may include Institutional Runaround, Branch, Convergence, Judicial Re-entry, Decision Stall, Referral-to-Uptake Latency, Resolution Latency, Translation Loss, Remedy Competition, Remedy Reframing, Responsibility Vacuum, and Cycle Closure.

Derived coding must remain reproducible from identified observations and must not overwrite the primary record.
