# DIBO — Democratic Institutional Behavior Observatory

> DIBO longitudinally follows public issues as they move across legislative, administrative, and judicial institutions.

**Current stage: DIBO Pilot / methodological development phase.** The protocol and data model are under development and should not be treated as validated.

## Follow the issue

Institutions are commonly studied as units. DIBO instead reconstructs the lineage of the issue across institutional boundaries.

The primary unit of observation is an **Issue Lineage**: the longitudinal history of the same public problem as it moves through public institutions.

## Three Lines

- `L` — Legislative
- `A` — Administrative
- `J` — Judicial

A Line records where an Episode occurred. Movement between Lines does not by itself indicate progress or resolution.

## Minimal data model

```text
Issue Lineage
    → Episode
    → Transition
    → Episode
    → Outcome
```

An **Episode** is a source-grounded event. A **Transition** connects two Episodes. An **Outcome** is the observed result or next step of an Episode; a response is not necessarily a resolution.

An Issue Lineage may branch, converge, return to a previous Line, or remain unresolved. Contributors record the underlying observations and do not need to classify these advanced patterns. Analytical variables are derived separately under [`analysis/`](analysis/README.md).

## Repository guide

- [`PROTOCOL.md`](PROTOCOL.md) — research principles and observation rules
- [`CODEBOOK.md`](CODEBOOK.md) — canonical fields and definitions
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — simple contribution instructions
- [`data/`](data/) — primary observational tables
- [`cases/`](cases/) — case documentation and source notes
- [`corrections/`](corrections/) — traceable corrections
- [`LICENSING.md`](LICENSING.md) — current licensing status

The initial case pages are templates only. They do not yet assert case facts, dates, citations, or current statuses.

## Relationship to MIBO

DIBO and MIBO are independent observatory programs. They share an interest in longitudinal, source-grounded, corrigible observation, but neither repository depends on the other.

## Licensing

Licensing is intentionally pending. See [`LICENSING.md`](LICENSING.md); absence of a license does not grant unrestricted permission to reuse repository content.
