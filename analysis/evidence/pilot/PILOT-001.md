# DIBO Evidence Coding Reliability Pilot 001

Status:

**PREREGISTERED – NOT YET CONDUCTED**

## Purpose

Pilot 001 is a methodological feasibility and inter-rater reliability pilot for Evidence Coding Protocol v0.1. Its primary purpose is to determine whether two independent human coders can apply the four evidence concepts reproducibly to the same frozen Assessment Scope and source packet.

Pilot 001 is not construct validation, generalizability validation, an Institutional Runaround assessment, or an institutional performance assessment.

## Frozen instrument

| Item | Frozen value |
| --- | --- |
| Evidence Protocol | `v0.1` |
| Pilot Kit | `v0.1` |
| Tag | `evidence-pilot-kit-v0.1` |
| Instrument/canonical-data commit | `e0f0c494680a4baf08a30c30e6a6633c979f2b8c` |

## Assessment Scope

- `scope_id`: `DIBO-RP-001`
- `issue_id`: `DIBO-JP-0004`
- `tracked_matter`: Whether spouses may retain their respective pre-marriage legal surnames upon marriage under Japanese law.

Included Episodes:

- `DIBO-JP-0004-E001`
- `DIBO-JP-0004-E002`
- `DIBO-JP-0004-E003`
- `DIBO-JP-0004-E004`
- `DIBO-JP-0004-E005`
- `DIBO-JP-0004-E006`
- `DIBO-JP-0004-E007`

Included Transitions:

- `DIBO-JP-0004-T001`
- `DIBO-JP-0004-T002`
- `DIBO-JP-0004-T003`
- `DIBO-JP-0004-T004`
- `DIBO-JP-0004-T005`
- `DIBO-JP-0004-T006`
- `DIBO-JP-0004-T007`
- `DIBO-JP-0004-T008`

Expected records per coder:

```text
7 + (3 * 8) = 31
```

## Investigator-facing selection rationale

This scope was selected before evidence coding because it contains multiple institutional arenas and different observed institutional forms while remaining one coherent tracked matter. It includes judicial consideration, legislative proposals, ordinary committee routing, competing policy designs, and subsequent administrative or government policy activity.

This selection rationale is investigator-facing and must not be included in the coder packet. It makes no prediction about any evidence code or coding unit.

## Coders

Two human coders use the stable pseudonymous IDs `C01` and `C02`. The protocol does not require public disclosure of personal names.

Both coders must use the same frozen Assessment Scope, Evidence Coding Codebook, source packet, and instructions.

## Training

Before real coding:

- both coders read Evidence Coding Protocol v0.1;
- both coders read Evidence Coding Codebook v0.1;
- any discussion or training uses only synthetic examples;
- no `DIBO-JP-0004` coding unit may be discussed during training.

Training ratings are not included in Pilot 001 reliability.

## Coder source packet

The coder-facing packet must be neutral. It may contain:

- for Episodes: `episode_id`, date, Line, institution, and official source URL or URLs;
- for Transitions: `transition_id`, `from_episode`, `to_episode`, and `transition_date`.

It must not contain:

- `cases/JP-0004/README.md`;
- Transition notes from `data/transitions.csv`;
- `what_happened` from `data/episodes.csv`;
- `result_or_next_step` from `data/episodes.csv`;
- the investigator selection rationale;
- any prior evidence code;
- any Institutional Runaround discussion.

The frozen common source packet consists of the official source URLs already attached to the included canonical Episodes. Additional source discovery is not permitted during independent coding. If the frozen packet is insufficient for a categorical decision, coders follow the Evidence Coding Protocol, including use of `INDETERMINATE` where appropriate.

## AI rule

No generative AI assistance is permitted during Pilot 001 independent coding. This rule is stricter than the general Evidence Coding Protocol and is chosen to isolate human inter-rater reproducibility.

Coders may use ordinary browser navigation and PDF or document text search. No AI-generated passage selection, summarization, interpretation, or categorical suggestion may be shown to either coder before ratings are locked.

## Independence and locking

`C01` and `C02` code independently. Before both sheets are locked, there is no discussion of individual units, exchange of codes, or access to the other coder's sheet.

After completion, validate both sheets separately. Then lock both pre-adjudication files before reliability calculation.

## Primary reliability outputs

For each of the four evidence concepts separately, report:

- coding-unit count;
- exact agreement;
- code distribution by coder;
- disagreement count and list.

Cohen's kappa is secondary and is reported only when mathematically defined by the released Pilot Kit. Do not calculate a pooled or global kappa, and do not apply qualitative kappa labels.

## No pass/fail threshold

Pilot 001 has no numerical acceptance threshold. Its purpose is diagnostic. Any methodological revision after Pilot 001 must be justified from observed disagreement patterns and documented separately.

## Adjudication

Reliability is calculated before adjudication. After the reliability output is frozen, disagreements may be reviewed separately.

Preserve the `C01` pre-adjudication sheet, `C02` pre-adjudication sheet, reliability report, and any later adjudicated record as distinct artifacts. Never overwrite original ratings.

## Institutional Runaround boundary

Pilot 001 does not produce `ESTABLISHED`, `NOT_ESTABLISHED`, or an evaluative `INDETERMINATE` classification for Institutional Runaround. Do not infer Institutional Runaround from evidence codes.

Do not infer institutional success, failure, dysfunction, responsiveness, or progress.

## Execution environment

The actual pilot must run from a clean detached worktree or clean checkout at tag `evidence-pilot-kit-v0.1`, commit `e0f0c494680a4baf08a30c30e6a6633c979f2b8c`.

The filled scope JSON and coder sheets must live outside that Git checkout. This is necessary because the Pilot Kit verifies that `canonical_data_ref` equals the canonical checkout HEAD. The real scope JSON therefore uses:

```text
canonical_data_ref: e0f0c494680a4baf08a30c30e6a6633c979f2b8c
```

Do not commit the filled scope or coder sheets before running the pilot in the frozen checkout.

## Post-pilot status

Pilot 001 results, if later produced, do not by themselves validate the Evidence Coding framework. A later replication on another Assessment Scope may be required before stronger reliability claims.
