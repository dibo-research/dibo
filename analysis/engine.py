"""Dependency-free descriptive topology and temporal analysis for DIBO."""

from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Iterable, Sequence


DERIVED_PROTOCOL_VERSION = "v0.1"
ENGINE_VERSION = "v0.1"
LINES = ("L", "A", "J")
LINE_PAIRS = tuple(f"{from_line}->{to_line}" for from_line in LINES for to_line in LINES)
IDENTIFIER_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

ISSUE_FIELDS = (
    "issue_id",
    "title",
    "country",
    "issue_summary",
    "requested_change",
    "start_date",
    "current_status",
    "notes",
)
EPISODE_FIELDS = (
    "episode_id",
    "issue_id",
    "date",
    "line",
    "institution",
    "what_happened",
    "result_or_next_step",
    "source",
)
TRANSITION_FIELDS = (
    "transition_id",
    "issue_id",
    "from_episode",
    "to_episode",
    "transition_date",
    "notes",
)


class ValidationError(ValueError):
    """Raised when canonical input cannot be analyzed without repair."""


def _read_table(path: Path, expected_fields: Sequence[str]) -> list[dict[str, str]]:
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            if tuple(reader.fieldnames or ()) != tuple(expected_fields):
                raise ValidationError(
                    f"{path}: expected canonical header {','.join(expected_fields)}"
                )
            return [dict(row) for row in reader]
    except FileNotFoundError as exc:
        raise ValidationError(f"canonical input not found: {path}") from exc
    except UnicodeDecodeError as exc:
        raise ValidationError(f"{path}: input is not valid UTF-8") from exc
    except csv.Error as exc:
        raise ValidationError(f"{path}: malformed CSV: {exc}") from exc


def _validate_identifier(value: str | None, label: str) -> str:
    if value is None or not value or value != value.strip() or not IDENTIFIER_RE.fullmatch(value):
        raise ValidationError(f"malformed required identifier for {label}: {value!r}")
    return value


def _parse_date(value: str | None, label: str, *, required: bool = True) -> date | None:
    if not value:
        if required:
            raise ValidationError(f"invalid complete date for {label}: {value!r}")
        return None
    if not DATE_RE.fullmatch(value):
        raise ValidationError(f"invalid complete date for {label}: {value!r}")
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValidationError(f"invalid complete date for {label}: {value!r}") from exc


def _ensure_unique(rows: Iterable[dict[str, str]], field: str) -> None:
    seen: set[str] = set()
    for row in rows:
        value = row[field]
        if value in seen:
            raise ValidationError(f"duplicate {field}: {value}")
        seen.add(value)


def load_and_validate(data_dir: str | Path) -> tuple[
    list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]
]:
    """Read and validate the three canonical tables without modifying them."""

    directory = Path(data_dir)
    issues = _read_table(directory / "issues.csv", ISSUE_FIELDS)
    episodes = _read_table(directory / "episodes.csv", EPISODE_FIELDS)
    transitions = _read_table(directory / "transitions.csv", TRANSITION_FIELDS)

    for row_number, issue in enumerate(issues, start=2):
        _validate_identifier(issue.get("issue_id"), f"issues.csv row {row_number} issue_id")
        _parse_date(issue.get("start_date"), f"issue {issue['issue_id']} start_date")
    _ensure_unique(issues, "issue_id")
    issues_by_id = {row["issue_id"]: row for row in issues}

    for row_number, episode in enumerate(episodes, start=2):
        _validate_identifier(
            episode.get("episode_id"), f"episodes.csv row {row_number} episode_id"
        )
        _validate_identifier(
            episode.get("issue_id"), f"episode {episode['episode_id']} issue_id"
        )
        if episode["issue_id"] not in issues_by_id:
            raise ValidationError(
                f"episode {episode['episode_id']} refers to unknown issue_id "
                f"{episode['issue_id']}"
            )
        if episode.get("line") not in LINES:
            raise ValidationError(
                f"episode {episode['episode_id']} has invalid Line {episode.get('line')!r}; "
                "expected L, A, or J"
            )
        _parse_date(episode.get("date"), f"episode {episode['episode_id']} date")
    _ensure_unique(episodes, "episode_id")
    episodes_by_id = {row["episode_id"]: row for row in episodes}

    for row_number, transition in enumerate(transitions, start=2):
        transition_id = _validate_identifier(
            transition.get("transition_id"),
            f"transitions.csv row {row_number} transition_id",
        )
        issue_id = _validate_identifier(
            transition.get("issue_id"), f"transition {transition_id} issue_id"
        )
        from_episode = _validate_identifier(
            transition.get("from_episode"), f"transition {transition_id} from_episode"
        )
        to_episode = _validate_identifier(
            transition.get("to_episode"), f"transition {transition_id} to_episode"
        )
        if issue_id not in issues_by_id:
            raise ValidationError(
                f"transition {transition_id} refers to unknown issue_id {issue_id}"
            )
        for endpoint_name, endpoint_id in (
            ("from_episode", from_episode),
            ("to_episode", to_episode),
        ):
            if endpoint_id not in episodes_by_id:
                raise ValidationError(
                    f"transition {transition_id} {endpoint_name} refers to unknown Episode "
                    f"{endpoint_id}"
                )
            endpoint_issue = episodes_by_id[endpoint_id]["issue_id"]
            if endpoint_issue != issue_id:
                raise ValidationError(
                    f"transition {transition_id} {endpoint_name} {endpoint_id} belongs to "
                    f"issue_id {endpoint_issue}, not {issue_id}"
                )
        _parse_date(
            transition.get("transition_date"),
            f"transition {transition_id} transition_date",
            required=False,
        )
    _ensure_unique(transitions, "transition_id")

    return issues, episodes, transitions


def _git_ref(path: Path) -> str:
    try:
        completed = subprocess.run(
            ["git", "-C", str(path.resolve()), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            timeout=3,
        )
    except (FileNotFoundError, subprocess.SubprocessError, OSError):
        return "unknown"
    value = completed.stdout.strip()
    return value or "unknown"


def _latency_summary(values: list[int]) -> dict[str, int | float | None]:
    if not values:
        return {"count": 0, "max_days": None, "mean_days": None, "min_days": None}
    return {
        "count": len(values),
        "max_days": max(values),
        "mean_days": round(sum(values) / len(values), 2),
        "min_days": min(values),
    }


def _component_count(node_ids: list[str], adjacency: dict[str, set[str]]) -> int:
    remaining = set(node_ids)
    count = 0
    while remaining:
        count += 1
        stack = [min(remaining)]
        while stack:
            node_id = stack.pop()
            if node_id not in remaining:
                continue
            remaining.remove(node_id)
            stack.extend(sorted(adjacency[node_id] & remaining, reverse=True))
    return count


def derive_analysis(
    issues: list[dict[str, str]],
    episodes: list[dict[str, str]],
    transitions: list[dict[str, str]],
    *,
    as_of_date: date | None = None,
    selected_issues: Sequence[str] | None = None,
    analysis_code_ref: str = "unknown",
    canonical_data_ref: str = "unknown",
) -> dict[str, object]:
    """Derive deterministic Layer 1 and Layer 2 descriptions from validated rows."""

    issues_by_id = {row["issue_id"]: row for row in issues}
    if selected_issues:
        requested = set(selected_issues)
        unknown = sorted(requested - issues_by_id.keys())
        if unknown:
            raise ValidationError(f"unknown requested issue_id: {', '.join(unknown)}")
        issue_ids = sorted(requested)
    else:
        issue_ids = sorted(issues_by_id)

    episodes_by_issue: dict[str, list[dict[str, str]]] = {issue_id: [] for issue_id in issue_ids}
    for episode in episodes:
        if episode["issue_id"] in episodes_by_issue:
            episodes_by_issue[episode["issue_id"]].append(episode)

    transitions_by_issue: dict[str, list[dict[str, str]]] = {
        issue_id: [] for issue_id in issue_ids
    }
    for transition in transitions:
        if transition["issue_id"] in transitions_by_issue:
            transitions_by_issue[transition["issue_id"]].append(transition)

    output_issues: list[dict[str, object]] = []
    for issue_id in issue_ids:
        issue = issues_by_id[issue_id]
        issue_episodes = sorted(
            episodes_by_issue[issue_id], key=lambda row: row["episode_id"]
        )
        issue_transitions = sorted(
            transitions_by_issue[issue_id], key=lambda row: row["transition_id"]
        )
        episode_map = {row["episode_id"]: row for row in issue_episodes}

        indegree = {episode_id: 0 for episode_id in episode_map}
        outdegree = {episode_id: 0 for episode_id in episode_map}
        adjacency = {episode_id: set() for episode_id in episode_map}
        transition_counts = Counter({pair: 0 for pair in LINE_PAIRS})
        edge_rows: list[dict[str, object]] = []
        warnings: list[dict[str, str]] = []
        same_line_latencies: list[int] = []
        cross_line_latencies: list[int] = []

        for transition in issue_transitions:
            from_episode = episode_map[transition["from_episode"]]
            to_episode = episode_map[transition["to_episode"]]
            from_id = from_episode["episode_id"]
            to_id = to_episode["episode_id"]
            indegree[to_id] += 1
            outdegree[from_id] += 1
            adjacency[from_id].add(to_id)
            adjacency[to_id].add(from_id)

            from_line = from_episode["line"]
            to_line = to_episode["line"]
            same_line = from_line == to_line
            latency = (
                _parse_date(to_episode["date"], f"episode {to_id} date")
                - _parse_date(from_episode["date"], f"episode {from_id} date")
            ).days
            transition_counts[f"{from_line}->{to_line}"] += 1
            edge_rows.append(
                {
                    "cross_line": not same_line,
                    "edge_latency_days": latency,
                    "from_episode": from_id,
                    "from_line": from_line,
                    "same_line": same_line,
                    "to_episode": to_id,
                    "to_line": to_line,
                    "transition_id": transition["transition_id"],
                }
            )
            if latency < 0:
                warnings.append(
                    {
                        "code": "negative_edge_latency",
                        "message": (
                            f"transition {transition['transition_id']} has negative edge latency "
                            f"({latency} days)"
                        ),
                        "transition_id": transition["transition_id"],
                    }
                )
            elif same_line:
                same_line_latencies.append(latency)
            else:
                cross_line_latencies.append(latency)

        node_rows = [
            {
                "branch_node": outdegree[episode["episode_id"]] >= 2,
                "date": episode["date"],
                "episode_id": episode["episode_id"],
                "indegree": indegree[episode["episode_id"]],
                "institution": episode["institution"],
                "line": episode["line"],
                "multiple_incoming": indegree[episode["episode_id"]] >= 2,
                "outdegree": outdegree[episode["episode_id"]],
                "root": indegree[episode["episode_id"]] == 0,
                "sink": outdegree[episode["episode_id"]] == 0,
            }
            for episode in issue_episodes
        ]

        component_count = _component_count(list(episode_map), adjacency)
        if component_count > 1:
            warnings.append(
                {
                    "code": "multiple_weakly_connected_components",
                    "message": f"issue has {component_count} weakly connected components",
                }
            )

        episode_dates = [
            _parse_date(episode["date"], f"episode {episode['episode_id']} date")
            for episode in issue_episodes
        ]
        if episode_dates:
            lineage_span_days: int | None = (max(episode_dates) - min(episode_dates)).days
        else:
            lineage_span_days = None
            warnings.append(
                {
                    "code": "no_canonical_episodes",
                    "message": "issue has no canonical Episodes",
                }
            )

        start_date = _parse_date(issue["start_date"], f"issue {issue_id} start_date")
        if as_of_date is None:
            lineage_age_days: int | None = None
        else:
            lineage_age_days = (as_of_date - start_date).days
            if lineage_age_days < 0:
                raise ValidationError(
                    f"as-of date {as_of_date.isoformat()} precedes start_date "
                    f"{start_date.isoformat()} for issue {issue_id}"
                )

        episode_counts = Counter(episode["line"] for episode in issue_episodes)
        output_issues.append(
            {
                "cross_line_latency": _latency_summary(cross_line_latencies),
                "edges": edge_rows,
                "episode_count": len(issue_episodes),
                "episode_counts_by_line": {line: episode_counts[line] for line in LINES},
                "issue_id": issue_id,
                "lineage_age_days": lineage_age_days,
                "lineage_span_days": lineage_span_days,
                "nodes": node_rows,
                "same_line_latency": _latency_summary(same_line_latencies),
                "transition_count": len(issue_transitions),
                "transition_counts_by_line_pair": {
                    pair: transition_counts[pair] for pair in LINE_PAIRS
                },
                "warnings": warnings,
                "weakly_connected_components": component_count,
            }
        )

    return {
        "issues": output_issues,
        "metadata": {
            "analysis_code_ref": analysis_code_ref,
            "as_of_date": as_of_date.isoformat() if as_of_date else None,
            "canonical_data_ref": canonical_data_ref,
            "derived_protocol_version": DERIVED_PROTOCOL_VERSION,
            "engine_version": ENGINE_VERSION,
        },
    }


def analyze(
    data_dir: str | Path,
    *,
    as_of_date: date | None = None,
    selected_issues: Sequence[str] | None = None,
) -> dict[str, object]:
    """Load, validate, and derive a complete analysis document."""

    directory = Path(data_dir)
    engine_repository_root = Path(__file__).resolve().parent.parent
    issues, episodes, transitions = load_and_validate(directory)
    return derive_analysis(
        issues,
        episodes,
        transitions,
        as_of_date=as_of_date,
        selected_issues=selected_issues,
        analysis_code_ref=_git_ref(engine_repository_root),
        canonical_data_ref=_git_ref(directory),
    )


def render_json(result: dict[str, object]) -> str:
    """Return the stable machine-readable representation."""

    return json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def _argument_date(value: str) -> date:
    try:
        parsed = _parse_date(value, "--as-of-date")
    except ValidationError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc
    assert parsed is not None
    return parsed


def build_parser() -> argparse.ArgumentParser:
    repository_root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(
        description="Derive deterministic DIBO topology and temporal descriptions."
    )
    parser.add_argument("--as-of-date", type=_argument_date, metavar="YYYY-MM-DD")
    parser.add_argument("--issue", action="append", dest="issues", metavar="ISSUE_ID")
    parser.add_argument("--output", type=Path, metavar="PATH")
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=repository_root / "data",
        metavar="PATH",
        help="directory containing the three canonical CSV tables",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        rendered = render_json(
            analyze(
                args.data_dir,
                as_of_date=args.as_of_date,
                selected_issues=args.issues,
            )
        )
        if args.output:
            args.output.write_text(rendered, encoding="utf-8", newline="")
        else:
            sys.stdout.write(rendered)
    except (ValidationError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
