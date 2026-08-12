# DIBO Codebook

## General conventions

- Store primary observations only in the three canonical CSV files.
- Use stable identifiers that are never reassigned.
- Use `YYYY-MM-DD` when a complete date is supported. Do not invent precision.
- Use concise factual language.
- Prefer official primary-source URLs.
- Leave an optional field empty rather than inferring an unsupported value.

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
| `current_status` | Short factual status supported by the available record. |
| `notes` | Optional scope, boundary, or uncertainty note. |

Canonical header:

```csv
issue_id,title,country,issue_summary,requested_change,start_date,current_status,notes
```

## `data/episodes.csv`

One row represents one source-grounded event. This is the main observational table.

| Field | Definition |
| --- | --- |
| `episode_id` | Stable Episode identifier. |
| `issue_id` | Parent Issue Lineage identifier. |
| `date` | Date of the observed event. |
| `line` | Exactly one of `L`, `A`, or `J`. |
| `institution` | Institution or institutional body involved. |
| `what_happened` | Concise factual description of the event. |
| `result_or_next_step` | Observed result or what happened next. This may be an Outcome, but does not imply resolution. |
| `source` | Traceable source, preferably an official primary-source URL. |

Canonical header:

```csv
episode_id,issue_id,date,line,institution,what_happened,result_or_next_step,source
```

## `data/transitions.csv`

One row represents a supported connection between two Episodes.

| Field | Definition |
| --- | --- |
| `transition_id` | Stable Transition identifier. |
| `issue_id` | Parent Issue Lineage identifier. |
| `from_episode` | Origin Episode identifier. |
| `to_episode` | Destination Episode identifier. |
| `transition_date` | Date of the transition when supported. |
| `notes` | Optional factual note about the connection or uncertainty. |

Canonical header:

```csv
transition_id,issue_id,from_episode,to_episode,transition_date,notes
```

Contributors do not need to classify transitions as referrals, returns, branches, convergence, stalls, or cycles. Those patterns may be derived from the recorded edges.

## Lines

| Code | Meaning |
| --- | --- |
| `L` | Legislative institution or process |
| `A` | Administrative institution or process |
| `J` | Judicial institution or process |

Assign the Line according to where the Episode occurred, not according to a presumed cause or desired remedy.

## Outcome

Outcome is a canonical concept, but it is not a separate table in the initial scaffold. Record the observable result or next step in `episodes.csv` under `result_or_next_step`. An Outcome may be partial, procedural, implemented, reversed, or unresolved; describe only what the evidence supports.

## Derived analysis

Derived variables belong under [`analysis/`](analysis/README.md). They may include Institutional Runaround, Referral-to-Uptake Latency, Resolution Latency, Branch, Convergence, Judicial Re-entry, Stall, Open Cycle, Remedy Reframing, and Translation Loss.

Derived coding must remain reproducible from identified observations and must not overwrite the primary record.
