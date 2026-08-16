# DIBO Evidence Reliability Pilot Kit

Version: v0.1

## Purpose

This kit operationalizes the existing Evidence Coding Protocol for a future two-human-coder reliability pilot. It provides a scope template, deterministic blank coding sheets, completed-sheet validation, and reliability calculation. It contains no pilot results.

## Workflow

1. Copy, complete, and freeze `scope.template.json` outside this template directory.
2. Generate one blank sheet per coder.
3. Have both humans code independently without AI categorical recommendations.
4. Lock ratings before discussion.
5. Validate both completed sheets.
6. Calculate reliability from the pre-adjudication sheets.
7. Adjudicate separately outside this tool.

Do not use adjudicated ratings as the two independent reliability inputs. The tool cannot prove independence; the study procedure must establish a frozen scope, independent coding, locked ratings before discussion, and no AI categorical recommendations before locking.

## Commands

```text
python analysis/evidence/pilot/pilot.py generate --scope PATH/TO/scope.json --coder-id C01 --data-dir data --output PATH/TO/C01.csv
python analysis/evidence/pilot/pilot.py validate --scope PATH/TO/scope.json --sheet PATH/TO/C01.csv --data-dir data
python analysis/evidence/pilot/pilot.py reliability --scope PATH/TO/scope.json --sheet-a PATH/TO/C01.csv --sheet-b PATH/TO/C02.csv --data-dir data --output PATH/TO/reliability.json
```

Run the tests with:

```text
python -m unittest discover -s analysis/evidence/pilot -p "test_*.py"
```

## Completeness rule

For `E` included Episodes and `T` included Transitions, each coder completes exactly:

```text
E + (3 * T)
```

## Reliability output

The deterministic report gives exact agreement, coder-specific code distributions, disagreement counts and records, and concept-specific Cohen's kappa when mathematically defined. It never pools concepts into a global kappa.

## Boundaries

This offline kit performs no automatic evidence coding, AI categorical recommendation, adjudication, Institutional Runaround classification, or performance assessment. The Evidence Coding Protocol governs permissible AI assistance outside this tool.
