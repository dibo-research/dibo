# DIBO Evidence Coding Automation Feasibility Run 001

Status:

**REGISTERED – NOT YET CONDUCTED**

## Purpose

Automation Feasibility Run 001 tests whether one operator can use one generative AI model to produce a structurally complete, source-referenced Evidence Coding sheet for a frozen Assessment Scope and then validate it with the released Pilot Kit.

Its purpose is operational feasibility and traceability. It is not:

- human inter-rater reliability;
- model-to-model agreement;
- evidence-code accuracy or construct validation;
- generalizability validation;
- Institutional Runaround assessment;
- institutional performance assessment.

## Frozen instrument and scope

| Item | Frozen value |
| --- | --- |
| Evidence Protocol | `v0.1` |
| Evidence Codebook | `v0.1` |
| Pilot Kit | `v0.1` |
| Tag | `evidence-pilot-kit-v0.1` |
| Instrument/canonical-data commit | `e0f0c494680a4baf08a30c30e6a6633c979f2b8c` |
| Scope ID | `DIBO-RP-001` |
| Issue ID | `DIBO-JP-0004` |

Tracked matter:

> Whether spouses may retain their respective pre-marriage legal surnames upon marriage under Japanese law.

The scope contains the seven Episodes and eight Transitions listed in `PILOT-001.md`. The expected sheet contains exactly:

```text
7 + (3 * 8) = 31 records
```

## Roles

- `OP01`: the single human operator who prepares frozen inputs, starts the run, preserves artifacts, and performs structural validation.
- `AI01`: the single generative AI coder that assigns all categorical evidence codes and produces the associated source fields and rationales.

`OP01` does not independently assign or silently edit evidence codes. Any later human-reviewed dataset must be stored separately and must not replace the original `AI01` output.

No second human coder or second AI model is used in Automation 001.

## Model freeze and run manifest

Before `AI01` receives the source packet, `OP01` records a simple external run manifest containing:

- provider and exact model identifier shown by the runtime;
- the exact instructions supplied to the model;
- Pilot Kit tag and commit;
- `scope_id`, `issue_id`, and `canonical_data_ref`.

After execution, `OP01` records whether a retry occurred and identifies the preserved raw response, generated sheet, and validation output.

The manifest and run artifacts live outside the Git checkout. Hosted-model output is not assumed to be bit-for-bit reproducible.

## Neutral source packet

`AI01` receives the same neutral packet defined for the original Pilot 001 scope. It may contain:

- for Episodes: `episode_id`, date, Line, institution, and official source URL or URLs;
- for Transitions: `transition_id`, `from_episode`, `to_episode`, and `transition_date`;
- Evidence Coding Protocol v0.1 and Codebook v0.1;
- the frozen tracked matter and eligible unit IDs.

It must not contain:

- `cases/JP-0004/README.md`;
- Transition notes from `data/transitions.csv`;
- `what_happened` or `result_or_next_step` from `data/episodes.csv`;
- the investigator selection rationale;
- any prior evidence code or expected answer;
- any Institutional Runaround discussion.

The common evidence packet is limited to the official source URLs already attached to the included canonical Episodes. `AI01` may navigate, search, read, select passages from, summarize, and interpret material within that frozen packet. Additional source discovery is not permitted.

## Automated coding procedure

1. Use a clean detached worktree or clean checkout at `evidence-pilot-kit-v0.1` (`e0f0c494680a4baf08a30c30e6a6633c979f2b8c`).
2. Keep the filled scope JSON, source packet, run manifest, prompt, raw model output, and coding sheet outside the checkout.
3. Set `canonical_data_ref` to `e0f0c494680a4baf08a30c30e6a6633c979f2b8c`.
4. Generate a blank 31-record sheet with coder ID `AI01` using the released `generate` command.
5. Give `AI01` the frozen instructions, scope, neutral packet, and blank sheet.
6. Require `AI01` to complete every expected record with one permitted evidence code, source fields, and a concise source-grounded rationale.
7. Preserve the raw model response before transforming it into the CSV sheet.
8. Run the released `validate` command on the completed `AI01` sheet.
9. Lock the original generated sheet and validation output before any human review.

The `reliability` command is not used because Automation 001 has only one coder.

No AI integration, model API call, or automatic categorical coding is added to `pilot.py`. Its released `generate` and `validate` functions remain deterministic and offline; `AI01` is operated separately and supplies the completed sheet.

## Failure and retry rule

An API, transport, context-limit, malformed-output, or structural-validation failure may be retried. Every attempt must be preserved and numbered.

A retry may add only mechanical formatting clarification needed to obtain the required schema. It must not add an expected category, unit-specific hint, investigator judgment, or new source. The first structurally valid complete sheet is the registered `AI01` output.

## Outputs

Automation 001 preserves, outside the Git checkout:

- frozen scope and source packet;
- run manifest and exact prompt;
- every raw model attempt;
- the first structurally valid `AI01` coding sheet;
- validation output;
- a short execution log describing failures, retries, and operator interventions.

The run may report record completeness, structural validation status, execution failures, retry count, and the categorical code distribution. It does not calculate exact inter-rater agreement, disagreements between raters, or Cohen's kappa.

## Human review boundary

Human review may occur only after the original `AI01` sheet is locked. Review may identify source, interpretation, or recording concerns, but any changed code belongs in a separate reviewed artifact. It must never overwrite or be presented as the original automated output.

Automation 001 does not establish that an AI-generated evidence code is correct. It tests whether the workflow can produce a complete, traceable, protocol-shaped artifact under the frozen conditions.

## Institutional Runaround boundary

No evidence code, distribution, or reviewed output from Automation 001 classifies Institutional Runaround. Do not infer institutional success, failure, dysfunction, responsiveness, or progress.

## Future comparison

A second AI model may be studied later under a separate registered design. Any such comparison is model-to-model agreement, not human inter-rater reliability, and is outside Automation 001.
