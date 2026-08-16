# DIBO Evidence Coding Codebook

## General coding rule

Code only the frozen Assessment Scope and the tracked matter stated in it. Anchor every record to an eligible canonical Episode or Transition and to source-grounded evidence. Do not infer a code from graph position, elapsed time, chronological succession, or institutional outcome alone.

The evidence concepts are independent questions. Assign each applicable concept separately; never use one code as an automatic substitute for another or as an Institutional Runaround classification.

## YES / NO / INDETERMINATE

- `YES`: the available evidence positively supports the concept for the coding unit and tracked matter.
- `NO`: the evidence is adequate and supports that the concept is not satisfied for the coding unit and tracked matter.
- `INDETERMINATE`: evidence is insufficient, ambiguous, internally conflicting, or insufficiently specific for `YES` or `NO`.

Absence of positive evidence, silence, and missing evidence are not automatically `NO`. Prefer `INDETERMINATE` whenever evidence adequacy is uncertain.

## DOCUMENTED_REDIRECTION

- **Unit:** `TRANSITION`.
- **YES:** source-grounded evidence shows that the actor associated with the relevant institutional step explicitly directs the tracked matter to another actor, refers or returns it elsewhere, transfers or reassigns handling, or states that another actor or institutional process should take it up.
- **NO:** evidence is adequate and shows that the Transition does not redirect the tracked matter to another actor or process.
- **INDETERMINATE:** the source does not establish whether a movement occurred, whether it was explicit, or whether it concerned the tracked matter.
- **Exclusions:** chronological succession, thematic continuity, and one institution acting after another are not redirection by themselves. Redirection does not automatically establish responsibility displacement, procedural impropriety, or Institutional Runaround.
- **Synthetic example:** Agency A states that Agency B handles request R and forwards R. This supports `DOCUMENTED_REDIRECTION = YES`. Whether authority was displaced or the route was procedurally necessary remains a separate source question.

## SUBSTANTIVE_DISPOSITION

- **Unit:** `EPISODE`.
- **YES:** the Episode contains an authoritative institutional action that materially addresses the tracked matter, such as granting or denying the request, issuing an authoritative determination, adopting or rejecting the assessed proposal, establishing or implementing the remedy, or resolving the responsibility question within the institution's authority.
- **NO:** evidence is adequate and shows that the Episode contains no authoritative action materially addressing the tracked matter.
- **INDETERMINATE:** the action, authority, or relationship to the tracked matter cannot be determined adequately from the available evidence.
- **Exclusions:** forwarding, receipt acknowledgment, scheduling review, directing another actor to decide, and procedural continuation are not automatically substantive dispositions. A favorable result is not required, and disposition of a tracked matter is not resolution of the whole Issue Lineage.
- **Synthetic example:** Court C issues an authoritative order denying petition P on its merits. This supports `SUBSTANTIVE_DISPOSITION = YES` even though the answer is negative; it says nothing by itself about resolution beyond P.

## PROCEDURALLY_NECESSARY_ROUTING

- **Unit:** `TRANSITION`.
- **YES:** an identifiable statute, procedural rule, formal competence allocation, ordinary appellate structure, formally required legislative or administrative stage, or required implementation step supports the routing toward competent consideration or implementation.
- **NO:** evidence is adequate and shows that the routing is not required or meaningfully explained by an identifiable ordinary, legal, or formal path.
- **INDETERMINATE:** the route appears possible or familiar, but evidence does not adequately establish why it is procedurally appropriate or inappropriate for the tracked matter.
- **Exclusions:** familiarity, chronology, and movement alone are insufficient. Procedural necessity does not establish progress, institutional success, or absence of responsibility displacement.
- **Synthetic example:** Committee B sends proposal Q to a required review stage identified in Rule 7. The cited rule can support `PROCEDURALLY_NECESSARY_ROUTING = YES`; substantive disposition and responsibility displacement require separate evidence.

## RESPONSIBILITY_DISPLACEMENT

- **Unit:** `TRANSITION`.
- **YES:** source-grounded evidence supports that an actor positions substantive authority or responsibility for the tracked matter elsewhere while not providing a substantive disposition within the relevant step. This may include expressly denying responsibility and naming another actor, declining substantive handling because another institution must decide, or transferring responsibility without retaining a substantive decision role.
- **NO:** evidence is adequate and shows that the actor does not position substantive authority or responsibility elsewhere, or that a documented handoff retains or properly executes the actor's relevant substantive role without displacement.
- **INDETERMINATE:** evidence does not adequately establish the actor's claimed authority, retained role, or substantive treatment of the tracked matter.
- **Exclusions:** do not infer bad faith, strategic avoidance, or political motive. A formal referral or documented redirection is not automatically responsibility displacement.
- **Synthetic example:** Agency A states that only Agency B may decide request R and declines to decide R. This may support `RESPONSIBILITY_DISPLACEMENT = YES` if the frozen scope and sources establish the relevant responsibility. Procedural necessity must still be coded from separate evidence.

## Cross-code distinctions

| Distinction | Coding consequence |
| --- | --- |
| Redirection is not displacement | `DOCUMENTED_REDIRECTION = YES` does not determine `RESPONSIBILITY_DISPLACEMENT`. |
| Redirection is not Runaround | A documented handoff does not classify Institutional Runaround. |
| A negative decision is not no disposition | An authoritative denial may be `SUBSTANTIVE_DISPOSITION = YES`. |
| Disposition is not whole-issue resolution | Code only the tracked matter, not the outcome of the entire Issue Lineage. |
| Routing is not progress | `PROCEDURALLY_NECESSARY_ROUTING = YES` is not a performance or progress judgment. |
| Procedural routing is not responsibility displacement | A formally justified route and displacement answer different evidence questions. |
| Missing evidence is not `NO` | Use `INDETERMINATE` when evidence is inadequate. |
| `INDETERMINATE` is not disagreement | Matching independent `INDETERMINATE` ratings count as agreement. |
| Evidence coding is not evaluative assessment | No evidence code, alone or in combination here, produces a Runaround classification. |
| AI-assisted retrieval is not independent human coding | A human must assign or explicitly verify final codes; an AI agent is not a human coder. |
