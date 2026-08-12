# Contributing to DIBO

You do not need to learn DIBO's full analytical framework to contribute a source-grounded observation.

## What to identify

To contribute an observation, identify:

1. the Issue Lineage;
2. the date;
3. whether the event occurred in the Legislative (`L`), Administrative (`A`), or Judicial (`J`) Line;
4. the institution;
5. what happened;
6. what happened next; and
7. the source.

The central research team will handle advanced analytical coding.

## How to contribute

1. Read the short rules in [`PROTOCOL.md`](PROTOCOL.md).
2. Check [`data/issues.csv`](data/issues.csv) for the relevant Issue Lineage.
3. Add the observation to [`data/episodes.csv`](data/episodes.csv), following [`CODEBOOK.md`](CODEBOOK.md).
4. Add a row to [`data/transitions.csv`](data/transitions.csv) only when the connection between two Episodes is supported.
5. Submit the change for review with a brief explanation of the source and scope.

If the Issue Lineage does not yet exist, propose its title, scope, requested change, and earliest supported date. Do not populate uncertain facts merely to complete every field.

## Small example

The following is a field template, not a factual DIBO record:

```text
episode_id: DIBO-XX-0001-E001
issue_id: DIBO-XX-0001
date: YYYY-MM-DD
line: A
institution: <official institution name>
what_happened: <one source-grounded sentence>
result_or_next_step: <observed result or next step>
source: <official primary-source URL>
```

## Before submitting

- Confirm that the event belongs to the stated Issue Lineage.
- Use only `L`, `A`, or `J` for `line`.
- Separate observed facts from interpretation.
- Prefer primary institutional sources.
- Do not infer hidden intent or describe a response as a resolution without evidence.
- Log corrections in [`corrections/correction_log.csv`](corrections/correction_log.csv).

Questions about boundaries or uncertain evidence are welcome in the proposed change. A transparent uncertainty note is preferable to unsupported precision.
