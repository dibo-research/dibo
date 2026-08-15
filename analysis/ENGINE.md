# DIBO Derived Descriptive Engine

**Version: v0.1**

The engine implements deterministic Layer 1 descriptive topology and Layer 2 temporal description from the canonical DIBO tables. It validates the inputs, constructs one directed graph per Issue Lineage, and emits stable JSON containing counts, node and edge descriptors, weakly connected component counts, observed lineage spans, and simple latency summaries.

**The engine does not classify Institutional Runaround.** Layer 3 evaluative constructs and institutional performance inference are outside its scope. Topology describes structure. Temporal measures describe elapsed observed time. Neither is an institutional quality score.

## Inputs and validation

The engine reads, but never writes, these canonical files:

- `data/issues.csv`
- `data/episodes.csv`
- `data/transitions.csv`

It fails with a non-zero exit code for invalid canonical headers, identifiers, Lines, dates, duplicates, unknown parents or endpoints, and cross-lineage Transition endpoints. It does not require one root, one sink, connectivity, or acyclicity.

## Output

JSON is written to stdout by default, with two-space indentation and sorted keys. Issues are ordered by `issue_id`, nodes by `episode_id`, and edges by `transition_id`. `--output` writes the same representation to a file. No output file is created by default.

`lineage_age_days` is `null` unless an explicit `--as-of-date` is supplied. An as-of date before a selected Issue's `start_date` is a validation error.

Metadata records two independent Git references when available. `analysis_code_ref` identifies the exact engine repository state containing `analysis/engine.py`; `canonical_data_ref` identifies the repository state containing the analyzed canonical data. The two may differ when `--data-dir` selects data from another Git checkout. Either value is `unknown` when its Git metadata is unavailable. Metadata also records `derived_protocol_version`, `engine_version`, and the explicit `as_of_date` or `null`.

Latency summaries contain `count`, `min_days`, `max_days`, and `mean_days`; means are rounded to two decimal places. Negative edge latency remains visible on the edge and produces a Transition-specific data-integrity warning, but is excluded from summary statistics. Structural warnings, including multiple weakly connected components and an Issue with no canonical Episodes, are observations rather than evaluations.

## CLI

```sh
python analysis/engine.py
python analysis/engine.py --as-of-date 2026-08-15
python analysis/engine.py --issue DIBO-JP-0002 --as-of-date 2026-08-15
python analysis/engine.py --output /tmp/dibo-derived.json
```

For synthetic fixtures or another compatible checkout, `--data-dir PATH` selects the directory containing the three canonical CSV files.

## Tests

The test suite uses only the Python standard library and creates synthetic canonical fixtures in temporary directories:

```sh
python -m unittest analysis.test_engine
```

No current DIBO case is used as a normative unit-test fixture.
