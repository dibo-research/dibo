# DIBO Research Protocol

## Purpose

DIBO reconstructs how a public issue moves across legislative, administrative, and judicial institutions. The protocol favors simple source-grounded observations at contribution time and reserves advanced interpretation for later analysis.

This is a pilot protocol in methodological development. Its reliability, coverage, and analytical validity have not yet been established.

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

Movement from one institution or Line to another does not automatically mean progress toward resolution.

### 3. A response is not a resolution

A reply, hearing, judgment, law, or announcement does not automatically resolve the underlying issue. Record what occurred and what followed without upgrading a response into a resolution.

### 4. Separate observation from interpretation

Record factual events first. Store analytical interpretations separately or derive them later from the primary observational tables.

### 5. Evidence first

Every substantive Episode should have a traceable source. Prefer sources in this order:

1. statutes and official legal texts;
2. court judgments and decisions;
3. parliamentary records;
4. official administrative documents;
5. other primary institutional records.

Secondary reporting may supplement primary evidence, but should not replace it when an appropriate primary source is available.

### 6. Do not infer hidden intent

Do not record political motive, institutional bad faith, hidden strategy, or responsibility unless evidence appropriate to that claim supports it. Describe observable conduct and documented statements.

### 7. Keep corrections traceable

Do not silently rewrite the historical record. Amend the relevant record and add an entry to [`corrections/correction_log.csv`](corrections/correction_log.csv) describing the change and its basis.

## Observation workflow

1. Define the Issue Lineage and its scope.
2. Add or verify the lineage in [`data/issues.csv`](data/issues.csv).
3. Record each supported event in [`data/episodes.csv`](data/episodes.csv).
4. Connect supported event sequences in [`data/transitions.csv`](data/transitions.csv).
5. Record the observed result or next step without assuming final resolution.
6. Keep case notes and source review in the relevant directory under [`cases/`](cases/).

Use the field definitions in [`CODEBOOK.md`](CODEBOOK.md).

## Primary observation and derived analysis

The files in [`data/`](data/) contain primary observations. They should remain factual, concise, and traceable to sources.

Advanced concepts—including runaround, latency, branches, convergence, judicial re-entry, stalls, cycles, remedy reframing, and translation loss—may be derived later under [`analysis/`](analysis/README.md). They must not be imposed on contributors as required classifications.

## Scope and uncertainty

An Issue Lineage requires an explicit boundary. When identity, sequence, or outcome is uncertain, record the uncertainty in notes and avoid unsupported linkage. Missing evidence is not evidence of institutional inaction.
