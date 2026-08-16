"""Deterministic utilities for a two-coder DIBO evidence reliability pilot."""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import tempfile
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable


PILOT_KIT_VERSION = "v0.1"
EVIDENCE_PROTOCOL_VERSION = "v0.1"

SHEET_HEADER = [
    "scope_id",
    "coder_id",
    "unit_type",
    "unit_id",
    "concept",
    "code",
    "source_ref",
    "source_locator",
    "rationale",
]

CONCEPTS = [
    "DOCUMENTED_REDIRECTION",
    "SUBSTANTIVE_DISPOSITION",
    "PROCEDURALLY_NECESSARY_ROUTING",
    "RESPONSIBILITY_DISPLACEMENT",
]

TRANSITION_CONCEPTS = [
    "DOCUMENTED_REDIRECTION",
    "PROCEDURALLY_NECESSARY_ROUTING",
    "RESPONSIBILITY_DISPLACEMENT",
]

CONCEPT_UNIT_TYPE = {
    "DOCUMENTED_REDIRECTION": "TRANSITION",
    "SUBSTANTIVE_DISPOSITION": "EPISODE",
    "PROCEDURALLY_NECESSARY_ROUTING": "TRANSITION",
    "RESPONSIBILITY_DISPLACEMENT": "TRANSITION",
}

CODES = ["YES", "NO", "INDETERMINATE"]


class PilotError(ValueError):
    """Raised when pilot input fails closed validation."""


@dataclass(frozen=True)
class Scope:
    scope_id: str
    issue_id: str
    tracked_matter: str
    included_episode_ids: tuple[str, ...]
    included_transition_ids: tuple[str, ...]
    canonical_data_ref: str
    evidence_protocol_version: str


@dataclass(frozen=True)
class ValidatedSheet:
    coder_id: str
    codes_by_pair: dict[tuple[str, str, str], str]


def _require_nonempty_string(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PilotError(f"scope field {field} must be a non-empty string")
    return value


def _scope_id_list(value: Any, field: str) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise PilotError(f"scope field {field} must be an array")
    values: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise PilotError(f"scope field {field} must contain only non-empty strings")
        values.append(item)
    duplicates = sorted(item for item, count in Counter(values).items() if count > 1)
    if duplicates:
        label = "Episode" if field == "included_episode_ids" else "Transition"
        raise PilotError(f"duplicate included {label} ID: {duplicates[0]}")
    return tuple(values)


def load_scope(path: str | Path) -> Scope:
    try:
        with Path(path).open("r", encoding="utf-8") as handle:
            raw = json.load(handle)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise PilotError(f"cannot read scope JSON: {exc}") from exc
    if not isinstance(raw, dict):
        raise PilotError("scope JSON must contain an object")

    required = [
        "scope_id",
        "issue_id",
        "tracked_matter",
        "included_episode_ids",
        "included_transition_ids",
        "canonical_data_ref",
        "evidence_protocol_version",
    ]
    missing = [field for field in required if field not in raw]
    if missing:
        raise PilotError(f"scope is missing required field: {missing[0]}")

    version = _require_nonempty_string(
        raw["evidence_protocol_version"], "evidence_protocol_version"
    )
    if version != EVIDENCE_PROTOCOL_VERSION:
        raise PilotError(
            "scope evidence_protocol_version must be " + EVIDENCE_PROTOCOL_VERSION
        )

    return Scope(
        scope_id=_require_nonempty_string(raw["scope_id"], "scope_id"),
        issue_id=_require_nonempty_string(raw["issue_id"], "issue_id"),
        tracked_matter=_require_nonempty_string(raw["tracked_matter"], "tracked_matter"),
        included_episode_ids=_scope_id_list(
            raw["included_episode_ids"], "included_episode_ids"
        ),
        included_transition_ids=_scope_id_list(
            raw["included_transition_ids"], "included_transition_ids"
        ),
        canonical_data_ref=_require_nonempty_string(
            raw["canonical_data_ref"], "canonical_data_ref"
        ),
        evidence_protocol_version=version,
    )


def _read_canonical_rows(
    path: Path, required_fields: Iterable[str]
) -> list[dict[str, str]]:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            fields = reader.fieldnames
            if fields is None:
                raise PilotError(f"canonical file has no header: {path}")
            missing = [field for field in required_fields if field not in fields]
            if missing:
                raise PilotError(f"canonical file {path} is missing column {missing[0]}")
            rows = list(reader)
    except (OSError, UnicodeError, csv.Error) as exc:
        raise PilotError(f"cannot read canonical file {path}: {exc}") from exc
    if any(None in row or None in row.values() for row in rows):
        raise PilotError(f"canonical file has a malformed row: {path}")
    return rows


def _index_unique(
    rows: Iterable[dict[str, str]], id_field: str, label: str
) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        item_id = row[id_field]
        if item_id in result:
            raise PilotError(f"duplicate canonical {label} ID: {item_id}")
        result[item_id] = row
    return result


def validate_scope_against_data(scope: Scope, data_dir: str | Path) -> None:
    root = Path(data_dir)
    issues = _index_unique(
        _read_canonical_rows(root / "issues.csv", ["issue_id"]),
        "issue_id",
        "issue",
    )
    episodes = _index_unique(
        _read_canonical_rows(root / "episodes.csv", ["episode_id", "issue_id"]),
        "episode_id",
        "Episode",
    )
    transitions = _index_unique(
        _read_canonical_rows(
            root / "transitions.csv", ["transition_id", "issue_id"]
        ),
        "transition_id",
        "Transition",
    )

    if scope.issue_id not in issues:
        raise PilotError(f"unknown issue_id: {scope.issue_id}")
    for episode_id in scope.included_episode_ids:
        if episode_id not in episodes:
            raise PilotError(f"unknown included Episode ID: {episode_id}")
        actual_issue = episodes[episode_id]["issue_id"]
        if actual_issue != scope.issue_id:
            raise PilotError(
                f"included Episode {episode_id} belongs to issue_id {actual_issue}, "
                f"not {scope.issue_id}"
            )
    for transition_id in scope.included_transition_ids:
        if transition_id not in transitions:
            raise PilotError(f"unknown included Transition ID: {transition_id}")
        actual_issue = transitions[transition_id]["issue_id"]
        if actual_issue != scope.issue_id:
            raise PilotError(
                f"included Transition {transition_id} belongs to issue_id {actual_issue}, "
                f"not {scope.issue_id}"
            )


def expected_pairs(scope: Scope) -> list[tuple[str, str, str]]:
    pairs = [
        ("EPISODE", episode_id, "SUBSTANTIVE_DISPOSITION")
        for episode_id in sorted(scope.included_episode_ids)
    ]
    pairs.extend(
        ("TRANSITION", transition_id, concept)
        for transition_id in sorted(scope.included_transition_ids)
        for concept in TRANSITION_CONCEPTS
    )
    return pairs


def _atomic_write(path: str | Path, content: str) -> None:
    destination = Path(path)
    temp_path: Path | None = None
    try:
        destination.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            newline="",
            dir=destination.parent,
            prefix=".pilot-",
            delete=False,
        ) as handle:
            temp_path = Path(handle.name)
            handle.write(content)
        os.replace(temp_path, destination)
    except (OSError, UnicodeError) as exc:
        if temp_path is not None:
            try:
                temp_path.unlink(missing_ok=True)
            except OSError:
                pass
        raise PilotError(f"cannot write output {destination}: {exc}") from exc


def _csv_text(rows: Iterable[dict[str, str]]) -> str:
    from io import StringIO

    buffer = StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=SHEET_HEADER, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue()


def generate_sheet(
    scope_path: str | Path,
    coder_id: str,
    data_dir: str | Path,
    output_path: str | Path,
) -> None:
    if not isinstance(coder_id, str) or not coder_id.strip():
        raise PilotError("coder_id must be non-empty")
    scope = load_scope(scope_path)
    validate_scope_against_data(scope, data_dir)
    rows = [
        {
            "scope_id": scope.scope_id,
            "coder_id": coder_id,
            "unit_type": unit_type,
            "unit_id": unit_id,
            "concept": concept,
            "code": "",
            "source_ref": "",
            "source_locator": "",
            "rationale": "",
        }
        for unit_type, unit_id, concept in expected_pairs(scope)
    ]
    _atomic_write(output_path, _csv_text(rows))


def _read_sheet(path: str | Path) -> list[dict[str, str]]:
    try:
        with Path(path).open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames != SHEET_HEADER:
                raise PilotError("coding sheet header does not exactly match the required header")
            rows = list(reader)
    except (OSError, UnicodeError, csv.Error) as exc:
        raise PilotError(f"cannot read coding sheet {path}: {exc}") from exc
    if any(None in row or None in row.values() for row in rows):
        raise PilotError("coding sheet contains a malformed row")
    return rows


def _validate_sheet_for_scope(scope: Scope, sheet_path: str | Path) -> ValidatedSheet:
    rows = _read_sheet(sheet_path)
    expected = expected_pairs(scope)
    expected_set = set(expected)
    included_units = {
        ("EPISODE", unit_id) for unit_id in scope.included_episode_ids
    } | {("TRANSITION", unit_id) for unit_id in scope.included_transition_ids}
    coder_ids: set[str] = set()
    codes_by_pair: dict[tuple[str, str, str], str] = {}

    for row_number, row in enumerate(rows, start=2):
        if row["scope_id"] != scope.scope_id:
            raise PilotError(
                f"coding sheet row {row_number} scope_id does not match frozen scope"
            )
        coder_ids.add(row["coder_id"])
        concept = row["concept"]
        if concept not in CONCEPT_UNIT_TYPE:
            raise PilotError(f"coding sheet row {row_number} has unknown concept {concept!r}")
        unit_type = row["unit_type"]
        expected_unit_type = CONCEPT_UNIT_TYPE[concept]
        if unit_type != expected_unit_type:
            raise PilotError(
                f"coding sheet row {row_number} has unit_type {unit_type!r}; "
                f"{concept} requires {expected_unit_type}"
            )
        unit_id = row["unit_id"]
        if (unit_type, unit_id) not in included_units:
            raise PilotError(
                f"coding sheet row {row_number} uses a unit outside the frozen scope"
            )
        pair = (unit_type, unit_id, concept)
        if pair in codes_by_pair:
            raise PilotError(
                f"duplicate unit-concept pair: {unit_type}/{unit_id}/{concept}"
            )
        if pair not in expected_set:
            raise PilotError(f"extra unit-concept pair: {unit_type}/{unit_id}/{concept}")
        code = row["code"]
        if not code:
            raise PilotError(f"coding sheet row {row_number} has a blank code")
        if code not in CODES:
            raise PilotError(
                f"coding sheet row {row_number} has invalid categorical code {code!r}"
            )
        if not row["rationale"].strip():
            raise PilotError(f"coding sheet row {row_number} has a blank rationale")
        codes_by_pair[pair] = code

    if len(coder_ids) != 1:
        raise PilotError("coding sheet must contain exactly one coder_id")
    coder_id = next(iter(coder_ids))
    if not coder_id.strip():
        raise PilotError("coding sheet coder_id must be non-empty")

    missing = [pair for pair in expected if pair not in codes_by_pair]
    if missing:
        unit_type, unit_id, concept = missing[0]
        raise PilotError(f"missing unit-concept pair: {unit_type}/{unit_id}/{concept}")
    extra = [pair for pair in codes_by_pair if pair not in expected_set]
    if extra:
        unit_type, unit_id, concept = sorted(extra)[0]
        raise PilotError(f"extra unit-concept pair: {unit_type}/{unit_id}/{concept}")
    if len(rows) != len(expected):
        raise PilotError(
            f"coding sheet record count is {len(rows)}; expected {len(expected)}"
        )
    return ValidatedSheet(coder_id=coder_id, codes_by_pair=codes_by_pair)


def validate_completed_sheet(
    scope_path: str | Path, sheet_path: str | Path, data_dir: str | Path
) -> ValidatedSheet:
    scope = load_scope(scope_path)
    validate_scope_against_data(scope, data_dir)
    return _validate_sheet_for_scope(scope, sheet_path)


def _concept_result(
    concept: str,
    pairs: list[tuple[str, str, str]],
    coder_a: ValidatedSheet,
    coder_b: ValidatedSheet,
) -> dict[str, Any]:
    concept_pairs = [pair for pair in pairs if pair[2] == concept]
    unit_count = len(concept_pairs)
    distributions = {
        coder_a.coder_id: {code: 0 for code in CODES},
        coder_b.coder_id: {code: 0 for code in CODES},
    }
    disagreements: list[dict[str, str]] = []
    agreement_count = 0

    for unit_type, unit_id, pair_concept in concept_pairs:
        pair = (unit_type, unit_id, pair_concept)
        code_a = coder_a.codes_by_pair[pair]
        code_b = coder_b.codes_by_pair[pair]
        distributions[coder_a.coder_id][code_a] += 1
        distributions[coder_b.coder_id][code_b] += 1
        if code_a == code_b:
            agreement_count += 1
        else:
            disagreements.append(
                {
                    "unit_type": unit_type,
                    "unit_id": unit_id,
                    "coder_a": coder_a.coder_id,
                    "coder_a_code": code_a,
                    "coder_b": coder_b.coder_id,
                    "coder_b_code": code_b,
                }
            )

    disagreements.sort(key=lambda item: item["unit_id"])
    if unit_count == 0:
        exact_agreement: float | None = None
        kappa: float | None = None
        kappa_status = "NO_UNITS"
    else:
        exact_agreement = agreement_count / unit_count
        expected_numerator = sum(
            distributions[coder_a.coder_id][code]
            * distributions[coder_b.coder_id][code]
            for code in CODES
        )
        if expected_numerator == unit_count * unit_count:
            kappa = None
            kappa_status = "UNDEFINED_EXPECTED_AGREEMENT"
        else:
            observed = Fraction(agreement_count, unit_count)
            expected = Fraction(expected_numerator, unit_count * unit_count)
            rounded = round(float((observed - expected) / (1 - expected)), 6)
            kappa = 0.0 if rounded == 0 else rounded
            kappa_status = "CALCULATED"

    return {
        "coding_unit_count": unit_count,
        "agreement_count": agreement_count,
        "exact_agreement_proportion": exact_agreement,
        "disagreement_count": len(disagreements),
        "code_distribution_by_coder": distributions,
        "cohen_kappa": kappa,
        "cohen_kappa_status": kappa_status,
        "disagreements": disagreements,
    }


def calculate_reliability(
    scope_path: str | Path,
    sheet_a_path: str | Path,
    sheet_b_path: str | Path,
    data_dir: str | Path,
) -> dict[str, Any]:
    scope = load_scope(scope_path)
    validate_scope_against_data(scope, data_dir)
    first = _validate_sheet_for_scope(scope, sheet_a_path)
    second = _validate_sheet_for_scope(scope, sheet_b_path)
    if first.coder_id == second.coder_id:
        raise PilotError("reliability requires two different coder IDs")
    if set(first.codes_by_pair) != set(second.codes_by_pair):
        raise PilotError("coder sheets do not contain the same unit-concept pairs")

    coder_a, coder_b = sorted([first, second], key=lambda sheet: sheet.coder_id)
    pairs = expected_pairs(scope)
    return {
        "metadata": {
            "pilot_kit_version": PILOT_KIT_VERSION,
            "evidence_protocol_version": scope.evidence_protocol_version,
            "scope_id": scope.scope_id,
            "issue_id": scope.issue_id,
            "canonical_data_ref": scope.canonical_data_ref,
            "coder_ids": [coder_a.coder_id, coder_b.coder_id],
        },
        "concepts": {
            concept: _concept_result(concept, pairs, coder_a, coder_b)
            for concept in CONCEPTS
        },
    }


def reliability_json(report: dict[str, Any]) -> str:
    return json.dumps(report, ensure_ascii=False, indent=2) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate = subparsers.add_parser("generate", help="generate a blank coding sheet")
    generate.add_argument("--scope", required=True)
    generate.add_argument("--coder-id", required=True)
    generate.add_argument("--data-dir", required=True)
    generate.add_argument("--output", required=True)

    validate = subparsers.add_parser("validate", help="validate a completed coding sheet")
    validate.add_argument("--scope", required=True)
    validate.add_argument("--sheet", required=True)
    validate.add_argument("--data-dir", required=True)

    reliability = subparsers.add_parser(
        "reliability", help="calculate two-coder pre-adjudication reliability"
    )
    reliability.add_argument("--scope", required=True)
    reliability.add_argument("--sheet-a", required=True)
    reliability.add_argument("--sheet-b", required=True)
    reliability.add_argument("--data-dir", required=True)
    reliability.add_argument("--output")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "generate":
            generate_sheet(args.scope, args.coder_id, args.data_dir, args.output)
        elif args.command == "validate":
            validate_completed_sheet(args.scope, args.sheet, args.data_dir)
        else:
            report = calculate_reliability(
                args.scope, args.sheet_a, args.sheet_b, args.data_dir
            )
            output = reliability_json(report)
            if args.output:
                output_path = Path(args.output).resolve()
                protected = {
                    Path(args.sheet_a).resolve(),
                    Path(args.sheet_b).resolve(),
                }
                if output_path in protected:
                    raise PilotError("reliability output must not overwrite an input sheet")
                _atomic_write(args.output, output)
            else:
                sys.stdout.write(output)
    except PilotError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
