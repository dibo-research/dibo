# DIBO Reference Verification Snapshots

## Purpose

These snapshots are reproducibility artifacts generated from frozen DIBO code and canonical observations.

They are not substantive research findings, institutional rankings, or performance assessments.

## Snapshot v0.1

File: `derived-engine-v0.1.json`

- Engine tag: `derived-engine-v0.1`
- Release commit: `cdf777b1e34ffebb3617a3ca1504d698c196838e`
- Derived protocol: `v0.1`
- Engine: `v0.1`
- `as_of_date`: none
- Issue Lineages: `DIBO-JP-0001` through `DIBO-JP-0004`

## Reproduction

From a clean checkout at tag `derived-engine-v0.1`, run:

```text
python -m unittest analysis.test_engine
python analysis/engine.py
```

The second command's stdout should match `derived-engine-v0.1.json` byte-for-byte. `SHA256SUMS` provides an additional content-integrity check.

## Interpretation boundary

Topology describes structure. Temporal measures describe elapsed observed time. Neither is an institutional quality score.

Institutional Runaround is not classified in this snapshot.
