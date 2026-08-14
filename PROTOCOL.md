# DIBO Research Protocol

**Version: DIBO v1.0.1**

## Purpose

DIBO reconstructs how a public issue moves across legislative, administrative, and judicial institutions. The protocol favors simple source-grounded observations at contribution time and reserves advanced interpretation for later analysis.

Version 1.0.1 is a conservative clarification informed by the first four canonical Issue Lineages. DIBO remains a pilot protocol in methodological development; its reliability, coverage, and analytical validity have not been established.

## Canonical concepts

1. **Issue Lineage** — the longitudinal history of the same public problem.
2. **Line** — the institutional setting of an Episode: Legislative (`L`), Administrative (`A`), or Judicial (`J`).
3. **Episode** — a dated, source-grounded institutional event.
4. **Transition** — a documented connection from one Episode to another.
5. **Outcome** — the observed result or next step associated with an Episode.

These five concepts form the public-facing model. More complex classifications are optional derived analysis, not mandatory contributor fields.

## Core rules

### 1. Follow the issue

The unit of analysis is the Issue Lineage, not merely the institution. Define the public problem and its boundary before assembling its institutional history.

### 2. Movement is not progress

Movement from one institution or Line to another does not automatically mean progress toward resolution. More Transitions do not imply more progress; a branch does not imply dysfunction; and long duration or repeated consideration does not by itself establish runaround, failure, or stall.

### 3. A response is not a resolution

A reply, hearing, judgment, law, or announcement does not automatically resolve the underlying issue. Record what occurred and what followed without upgrading a response into a resolution.

### 4. Separate observation from interpretation

Record factual events first. Store analytical interpretations separately or derive them later from the primary observational tables. Chronology is not causality: do not describe a later Episode as caused by an earlier one solely because it followed it. Use narrower factual language such as “later institutional response,” “issue-level uptake,” or “subsequent implementation” when the evidence supports it.

### 5. Evidence first

Every substantive Episode should have a traceable source. Prefer sources in this order:

1. statutes and official legal texts;
2. court judgments and decisions;
3. parliamentary records;
4. official administrative documents;
5. other primary institutional records.

One Episode may cite more than one official source when those sources document the same event. Separate institutional acts must not be combined merely to reduce the source count. Secondary reporting may supplement primary evidence, but should not replace it when an appropriate primary source is available.

### 6. Do not infer hidden intent

Do not record political motive, institutional bad faith, hidden strategy, responsibility, formal transfer, or causation unless evidence appropriate to that claim supports it. Source URLs support the factual Episode; they do not establish hidden intent.

### 7. Keep corrections traceable

Do not silently rewrite the historical record. Amend the relevant record and add an entry to [`corrections/correction_log.csv`](corrections/correction_log.csv) describing the change and its basis.

## Episode inclusion and granularity

An Episode is a substantively meaningful, dated, source-grounded institutional event. A new Episode normally requires an observable institutional action or decision that materially changes the institutional state of the Issue Lineage.

Not every state change is an Episode. Do not create an Episode merely because time passed, a status changed automatically, a document restated an existing state, a statistic was updated, or political expectations changed.

Separate institutional acts should normally remain separate Episodes even when they occur on the same date, occur within the same institution, or reach similar conclusions. Do not aggregate separate decisions solely because their timing or outcomes are similar. Conversely, multiple source documents may support one Episode when they document the same institutional event.

One document does not necessarily equal one Episode. Prefer the smallest Episode set that preserves substantively meaningful institutional state changes. Intermediate hearings, meetings, filings, notices, or appeal steps may be omitted when they do not materially change that state and omission does not prevent reconstruction of the lineage. This is a relevance rule, not permission for arbitrary compression.

Materially different proposals addressing the same public problem remain separate Episodes when they are separate institutional actions, even if they are considered together or share a broad goal. A later common committee or institutional action may be recorded as its own Episode.

## Transition and graph rules

A Transition records a supported connection between Episodes. It may connect different Lines or the same Line: `J → J`, `A → A`, and `L → L` are valid. Transition is therefore more general than institutional handoff.

An Issue Lineage need not be a linear chain. The graph may contain multiple outgoing Transitions, multiple incoming Transitions, parallel institutional paths, and later common responses. Represent those structures directly as edges in [`data/transitions.csv`](data/transitions.csv); contributors do not need to label them as branches, convergence, merges, or cycles.

Do not combine distinct earlier Episodes merely to make a graph appear to converge. Preserve the observations and, when one later event responds to several of them, use separate incoming Transitions to that later Episode.

A statement that another institution should consider or decide an issue is not automatically a formal referral, legal transfer, or jurisdictional transfer. A Transition may record later issue-level uptake when the later event clearly concerns the same Issue Lineage, but its note must not imply formal referral or a single-cause relationship unless the evidence supports that exact characterization. Chronology and thematic continuity do not by themselves establish formal referral or causation.

## Line assignment

Assign the Line according to the institutional process in which the observable action occurred, not according to a presumed cause, desired remedy, or eventual destination.

- `L` includes legislative actions such as bill introduction, committee action, final enactment, and parliamentary budget authorization.
- `A` includes executive or administrative actions such as formal policy adoption, administrative implementation, and government preparation or submission activity where appropriate under the existing coding convention.
- `J` includes judicial judgments and decisions.

Do not add Line subtypes.

## Outcomes and current status

Outcome records the observable result or next step associated with an Episode; it does not imply final resolution. Outcomes may describe continuation, enactment, implementation, partial operation, non-adoption, pending action, reversal, or unresolved status.

A law's automatic commencement on a date already fixed by an enacted commencement clause is not necessarily a new Episode when no institution takes a new action on that date. Record such a directly related change in `result_or_next_step`, the Issue's `current_status`, or date-stamped case documentation. A later observable act, such as a Cabinet order fixing a commencement date, may qualify as a new Episode.

Keep `current_status` short, stable, and factual. Routinely changing operational counts and transient political commentary belong in date-stamped case documentation unless the count itself is the institutional event being studied. Do not rewrite a historical Episode each time cumulative statistics change.

## Observation workflow

1. Define the Issue Lineage and its scope.
2. Add or verify the lineage in [`data/issues.csv`](data/issues.csv).
3. Record each supported Episode in [`data/episodes.csv`](data/episodes.csv).
4. Connect supported Episode sequences in [`data/transitions.csv`](data/transitions.csv).
5. Record each observable Outcome without assuming final resolution.
6. Keep case notes, dated status, and source review in the relevant directory under [`cases/`](cases/).

Use the field definitions in [`CODEBOOK.md`](CODEBOOK.md).

## Primary observation and derived analysis

The files in [`data/`](data/) contain primary observations. They should remain factual, concise, and traceable to sources.

Institutional Runaround, Branch, Convergence, Judicial Re-entry, Decision Stall, Referral-to-Uptake Latency, Resolution Latency, Translation Loss, Remedy Competition, Remedy Reframing, Responsibility Vacuum, Cycle Closure, and related constructs may be derived later under [`analysis/`](analysis/README.md). They require explicit reproducible rules and must not be imposed on contributors as canonical classifications.

## Scope and uncertainty

An Issue Lineage requires an explicit boundary. When identity, sequence, or outcome is uncertain, record the uncertainty in notes and avoid unsupported linkage. Missing evidence is not evidence of institutional inaction.
