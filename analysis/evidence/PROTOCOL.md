# DIBO Evidence Coding Protocol

**Version: v0.1**

## Purpose

This protocol defines a reproducible, analyst-facing method for coding four source-grounded evidence concepts needed by later evaluative work:

- `DOCUMENTED_REDIRECTION`;
- `SUBSTANTIVE_DISPOSITION`;
- `PROCEDURALLY_NECESSARY_ROUTING`;
- `RESPONSIBILITY_DISPLACEMENT`.

These concepts are not canonical DIBO fields and are not automatically derivable from graph topology or elapsed time. They require source review. This protocol defines evidence inputs only; it neither classifies Institutional Runaround nor implements an evidence-coding engine.

Observe first. Describe second. Code evidence third. Evaluate last.

## Analytical position

DIBO primary observations record source-grounded institutional events. The Derived Descriptive Engine deterministically describes topology and elapsed observed time. Evidence Coding adds structured human interpretation of specific source-grounded questions required by later evaluative constructs.

```text
Canonical Observation
  -> Descriptive Topology + Time
  -> Evidence Coding
  -> Evaluative Assessment
```

Evidence Coding must not overwrite canonical observations or alter deterministic descriptive outputs. It is an analyst-facing layer, not a new contributor-facing requirement. Canonical contributors do not need to learn this evidence vocabulary, and no evidence code becomes canonical data automatically.

## Assessment Scope

Evidence must not be coded against an undifferentiated Issue Lineage. Before coding begins, define an Assessment Scope containing:

- `scope_id`;
- `issue_id`;
- `tracked_matter`;
- included Episode IDs;
- included Transition IDs;
- `canonical_data_ref`;
- `evidence_protocol_version`.

The `tracked_matter` must identify the concrete request, remedy, responsibility question, or explicitly limited aspect being assessed. A suitable form is: "Whether institution X accepted responsibility for deciding request Y." Vague formulations such as "the whole issue" or "whether institutions responded well" are not valid scopes.

For inter-coder exercises, the Assessment Scope is frozen before independent coding. Every coder receives the same eligible Episodes and Transitions and must not silently expand or shrink them. A coder who finds the scope materially incomplete records a scope concern. The team resolves that concern before final reliability analysis rather than allowing coders to use different case boundaries.

## Coding units

Evidence records use existing canonical units as anchors:

| Concept | Unit |
| --- | --- |
| `SUBSTANTIVE_DISPOSITION` | `EPISODE` |
| `DOCUMENTED_REDIRECTION` | `TRANSITION` |
| `PROCEDURALLY_NECESSARY_ROUTING` | `TRANSITION` |
| `RESPONSIBILITY_DISPLACEMENT` | `TRANSITION` |

Evidence coding must not invent primary Episodes or Transitions. A factual error discovered during coding belongs in the separate DIBO correction process.

## Evidence record

A future long-form evidence record contains:

- `scope_id`;
- `coder_id`;
- `unit_type`;
- `unit_id`;
- `concept`;
- `code`;
- `source_ref`;
- `source_locator`;
- `rationale`.

Allowed `unit_type` values are `EPISODE` and `TRANSITION`. Allowed concepts are the four concepts listed under Purpose. Allowed final evidence codes are exactly `YES`, `NO`, and `INDETERMINATE`. This protocol defines the logical record only; it does not create a CSV or metadata schema.

Each coding exercise should also record, at minimum, `canonical_data_ref`, `derived_analysis_protocol_version`, `evidence_coding_protocol_version`, `scope_id`, `issue_id`, `tracked_matter`, included units, `coder_id`, and source references. If deterministic engine output selects or displays units, also record `engine_version` and `analysis_code_ref`.

Use a stable `coder_id` within an exercise. Personal names need not be published; stable pseudonymous identifiers such as `C01` and `C02` are acceptable.

## Coding values

- `YES`: available evidence positively supports that the coding unit satisfies the concept for the tracked matter.
- `NO`: evidence is adequate for assessment and supports that the coding unit does not satisfy the concept for the tracked matter.
- `INDETERMINATE`: evidence is insufficient, ambiguous, internally conflicting, or insufficiently specific to support `YES` or `NO`.

Absence, silence, and missing evidence are not automatically `NO`. When evidence adequacy is uncertain, prefer `INDETERMINATE`.

`INDETERMINATE` is a substantive evidence state, not missing data automatically, coder failure, disagreement, or `NO`. Two coders independently assigning `INDETERMINATE` agree. A high proportion may indicate weak sources, an ill-defined scope, or a construct that is difficult to observe; it must not be automatically recoded during adjudication.

Operational definitions and exclusions appear in the [Codebook](CODEBOOK.md).

## Source standards

Use source-grounded evidence in this preferred order:

1. statutes and official legal texts;
2. judgments and court decisions;
3. parliamentary records;
4. official administrative documents;
5. other primary institutional records.

Secondary sources may assist discovery but should not replace available primary institutional evidence. Coding may use a canonical source attached to an Episode, a canonical source relevant to Transition context, or an additional official source found during coding. Additional evidence does not automatically become canonical data.

A URL alone may be insufficient for reproducible review. Each `YES` or `NO` should, where reasonably possible, include a precise page, paragraph, section, article, committee-record location, heading, or other stable `source_locator`. Long quotations are unnecessary. Prefer `source_ref` plus `source_locator` plus a concise factual rationale. An `INDETERMINATE` rationale should identify what is missing, ambiguous, conflicting, or insufficiently specific.

Every record must answer: "What in the source justifies this code for this tracked matter?" Rationales must avoid inferred motive, normative judgment, political evaluation, and speculation. For example, prefer "The document assigns authority for deciding X to institution Y and contains no substantive determination of X" over a claim that an institution was avoiding responsibility.

## Coding workflow

1. Define and freeze the Assessment Scope.
2. Fix the eligible units, source packet, or common source-access rules.
3. Train coders on separate records when feasible.
4. Have human coders work independently and lock their ratings before discussion.
5. Preserve and compare the pre-adjudication ratings.
6. Categorize disagreements and adjudicate them separately.
7. Report reliability by evidence concept.

Training may clarify scope interpretation, `YES` versus `INDETERMINATE`, formal referral versus responsibility displacement, and procedural routing versus substantive disposition. Do not repeatedly change the codebook while treating the same records as final reliability observations. If a material rule changes, version the protocol or restart the affected reliability exercise.

## Independent coding

Reliability studies require at least two human coders. They independently code the same frozen Assessment Scope, eligible units, source packet or source-access rules, and protocol version. Discussion of individual codes must wait until independent ratings are locked.

Single-coder exploratory work is permitted but cannot support an inter-rater reliability claim. Evidence coders should remain blind to, and must not assign or discuss, final Institutional Runaround classifications while coding evidence.

## Adjudication

After independent coding is locked, compare outputs. For each disagreement, identify whether it concerns scope, evidence availability, concept definition, source interpretation, or a recording error. Adjudication may use consensus discussion or a third human reviewer.

Preserve pre-adjudication ratings and the adjudicated result as separate analytical records. Never overwrite or back-edit the original independent ratings.

## Reliability reporting

For each evidence concept separately, report:

- number of coding units;
- exact agreement proportion;
- code distribution by coder;
- disagreement count.

With two coders and sufficient category variation, Cohen's kappa may also be reported. Do not pool all four concepts into one kappa. If kappa is undefined or unstable because one or more categories lack variation, report that condition explicitly rather than substituting an arbitrary value.

Version v0.1 establishes no universal acceptance threshold. It defines a coding method, not validated reliability standards.

## AI assistance

AI may assist document discovery, source navigation, candidate-passage extraction, and coding-sheet formatting. AI output must not silently become a final human evidence code. Final codes used for inter-rater reliability or evaluative research claims must be assigned or explicitly verified by human coders. An AI agent is not an independent human coder.

If AI materially assists retrieval or preparation, document that role in study methods.

## Separation from evaluative assessment

No single evidence code establishes Institutional Runaround. In particular:

- documented redirection does not establish responsibility displacement;
- documented redirection does not establish Institutional Runaround;
- procedurally necessary routing does not establish progress or institutional success;
- substantive disposition does not establish resolution of the whole Issue Lineage;
- responsibility displacement does not establish Institutional Runaround by itself.

This protocol defines no executable derivation of `ESTABLISHED`, `NOT_ESTABLISHED`, or an evaluative `INDETERMINATE` classification. Those decisions belong to a later assessment protocol.

## Reproducibility

A reproducible exercise freezes its scope and protocol version; records eligible canonical units and Git references; retains source references and locators; uses stable coder identifiers; preserves independent ratings; and separates any adjudicated result. Deterministic descriptive output may help select or display units, but it neither supplies evidence codes nor changes the evidentiary judgment.

## Status and limitations

DIBO Evidence Coding Protocol v0.1 is an initial methodological specification. It has not yet demonstrated inter-rater reliability, construct validity, generalizability, or accuracy of Institutional Runaround classification. The next empirical step is a separate reliability pilot; no pilot results or case-level codes are included here.
