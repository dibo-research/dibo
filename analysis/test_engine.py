"""Standard-library tests for the DIBO derived descriptive engine."""

from __future__ import annotations

import csv
import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr
from datetime import date
from pathlib import Path

from analysis import engine


def issue(issue_id: str = "TEST-001", start_date: str = "2020-01-01") -> dict[str, str]:
    return {
        "issue_id": issue_id,
        "title": "Synthetic issue",
        "country": "XX",
        "issue_summary": "Synthetic fixture",
        "requested_change": "Synthetic change",
        "start_date": start_date,
        "current_status": "Recorded",
        "notes": "",
    }


def episode(
    episode_id: str,
    day: str,
    line: str,
    issue_id: str = "TEST-001",
) -> dict[str, str]:
    return {
        "episode_id": episode_id,
        "issue_id": issue_id,
        "date": day,
        "line": line,
        "institution": f"Institution {episode_id}",
        "what_happened": "Synthetic event",
        "result_or_next_step": "Synthetic result",
        "source": "https://example.test/source",
    }


def transition(
    transition_id: str,
    from_episode: str,
    to_episode: str,
    issue_id: str = "TEST-001",
) -> dict[str, str]:
    return {
        "transition_id": transition_id,
        "issue_id": issue_id,
        "from_episode": from_episode,
        "to_episode": to_episode,
        "transition_date": "2020-01-02",
        "notes": "Synthetic edge",
    }


class Fixture:
    def __init__(
        self,
        issues: list[dict[str, str]],
        episodes: list[dict[str, str]],
        transitions: list[dict[str, str]],
    ) -> None:
        self._temporary = tempfile.TemporaryDirectory()
        self.path = Path(self._temporary.name)
        self._write("issues.csv", engine.ISSUE_FIELDS, issues)
        self._write("episodes.csv", engine.EPISODE_FIELDS, episodes)
        self._write("transitions.csv", engine.TRANSITION_FIELDS, transitions)

    def _write(
        self, filename: str, fields: tuple[str, ...], rows: list[dict[str, str]]
    ) -> None:
        with (self.path / filename).open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)

    def close(self) -> None:
        self._temporary.cleanup()


class EngineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixtures: list[Fixture] = []

    def tearDown(self) -> None:
        for fixture in self.fixtures:
            fixture.close()

    def analyze(
        self,
        episodes: list[dict[str, str]],
        transitions: list[dict[str, str]],
        *,
        issues: list[dict[str, str]] | None = None,
        as_of_date: date | None = None,
        selected_issues: list[str] | None = None,
    ) -> dict[str, object]:
        fixture = Fixture(issues or [issue()], episodes, transitions)
        self.fixtures.append(fixture)
        rows = engine.load_and_validate(fixture.path)
        return engine.derive_analysis(
            *rows,
            as_of_date=as_of_date,
            selected_issues=selected_issues,
            analysis_code_ref="test-engine-ref",
            canonical_data_ref="test-data-ref",
        )

    def test_simple_linear_cross_line_graph(self) -> None:
        result = self.analyze(
            [episode("E1", "2020-01-01", "L"), episode("E2", "2020-01-04", "A")],
            [transition("T1", "E1", "E2")],
        )["issues"][0]
        self.assertEqual(result["episode_count"], 2)
        self.assertEqual(result["transition_count"], 1)
        self.assertEqual(result["transition_counts_by_line_pair"]["L->A"], 1)
        self.assertTrue(result["edges"][0]["cross_line"])
        self.assertEqual(result["cross_line_latency"]["mean_days"], 3.0)

    def test_same_line_transition(self) -> None:
        result = self.analyze(
            [episode("E1", "2020-01-01", "J"), episode("E2", "2020-01-03", "J")],
            [transition("T1", "E1", "E2")],
        )["issues"][0]
        self.assertTrue(result["edges"][0]["same_line"])
        self.assertEqual(result["same_line_latency"]["count"], 1)
        self.assertEqual(result["transition_counts_by_line_pair"]["J->J"], 1)

    def test_branch_node(self) -> None:
        result = self.analyze(
            [
                episode("E1", "2020-01-01", "L"),
                episode("E2", "2020-01-02", "A"),
                episode("E3", "2020-01-03", "J"),
            ],
            [transition("T1", "E1", "E2"), transition("T2", "E1", "E3")],
        )["issues"][0]
        nodes = {node["episode_id"]: node for node in result["nodes"]}
        self.assertEqual(nodes["E1"]["outdegree"], 2)
        self.assertTrue(nodes["E1"]["branch_node"])

    def test_multiple_incoming_node(self) -> None:
        result = self.analyze(
            [
                episode("E1", "2020-01-01", "L"),
                episode("E2", "2020-01-01", "A"),
                episode("E3", "2020-01-03", "J"),
            ],
            [transition("T1", "E1", "E3"), transition("T2", "E2", "E3")],
        )["issues"][0]
        nodes = {node["episode_id"]: node for node in result["nodes"]}
        self.assertEqual(nodes["E3"]["indegree"], 2)
        self.assertTrue(nodes["E3"]["multiple_incoming"])

    def test_multiple_roots_and_disconnected_components(self) -> None:
        result = self.analyze(
            [episode("E1", "2020-01-01", "L"), episode("E2", "2020-01-02", "A")],
            [],
        )["issues"][0]
        self.assertEqual(result["weakly_connected_components"], 2)
        self.assertTrue(all(node["root"] and node["sink"] for node in result["nodes"]))
        self.assertEqual(result["transition_count"], 0)
        self.assertTrue(
            all(value == 0 for value in result["transition_counts_by_line_pair"].values())
        )

    def test_zero_day_edge_latency(self) -> None:
        result = self.analyze(
            [episode("E1", "2020-01-01", "L"), episode("E2", "2020-01-01", "A")],
            [transition("T1", "E1", "E2")],
        )["issues"][0]
        self.assertEqual(result["edges"][0]["edge_latency_days"], 0)
        self.assertEqual(result["cross_line_latency"]["min_days"], 0)

    def test_negative_edge_latency_warns_and_is_excluded_from_summary(self) -> None:
        result = self.analyze(
            [episode("E1", "2020-01-03", "L"), episode("E2", "2020-01-01", "A")],
            [transition("T1", "E1", "E2")],
        )["issues"][0]
        self.assertEqual(result["edges"][0]["edge_latency_days"], -2)
        self.assertEqual(result["cross_line_latency"]["count"], 0)
        self.assertEqual(result["warnings"][0]["code"], "negative_edge_latency")
        self.assertEqual(result["warnings"][0]["transition_id"], "T1")

    def test_lineage_span(self) -> None:
        result = self.analyze(
            [episode("E2", "2020-01-11", "A"), episode("E1", "2020-01-01", "L")],
            [],
        )["issues"][0]
        self.assertEqual(result["lineage_span_days"], 10)

    def test_single_episode_span_is_zero(self) -> None:
        result = self.analyze([episode("E1", "2020-01-01", "L")], [])["issues"][0]
        self.assertEqual(result["lineage_span_days"], 0)

    def test_explicit_as_of_date_lineage_age(self) -> None:
        result = self.analyze(
            [episode("E1", "2020-01-01", "L")],
            [],
            as_of_date=date(2020, 1, 11),
        )["issues"][0]
        self.assertEqual(result["lineage_age_days"], 10)

    def test_absent_as_of_date_does_not_use_system_date(self) -> None:
        result = self.analyze([episode("E1", "2020-01-01", "L")], [])["issues"][0]
        self.assertIsNone(result["lineage_age_days"])

    def test_unknown_transition_endpoint_fails(self) -> None:
        fixture = Fixture(
            [issue()],
            [episode("E1", "2020-01-01", "L")],
            [transition("T1", "E1", "MISSING")],
        )
        self.fixtures.append(fixture)
        with self.assertRaisesRegex(engine.ValidationError, "unknown Episode MISSING"):
            engine.load_and_validate(fixture.path)

    def test_duplicate_episode_id_fails(self) -> None:
        fixture = Fixture(
            [issue()],
            [episode("E1", "2020-01-01", "L"), episode("E1", "2020-01-02", "A")],
            [],
        )
        self.fixtures.append(fixture)
        with self.assertRaisesRegex(engine.ValidationError, "duplicate episode_id: E1"):
            engine.load_and_validate(fixture.path)

    def test_invalid_line_fails(self) -> None:
        fixture = Fixture([issue()], [episode("E1", "2020-01-01", "X")], [])
        self.fixtures.append(fixture)
        with self.assertRaisesRegex(engine.ValidationError, "invalid Line 'X'"):
            engine.load_and_validate(fixture.path)

    def test_unknown_requested_issue_fails(self) -> None:
        fixture = Fixture(
            [issue()],
            [episode("E1", "2020-01-01", "L")],
            [],
        )
        self.fixtures.append(fixture)
        errors = io.StringIO()
        with redirect_stderr(errors):
            exit_code = engine.main(
                ["--data-dir", str(fixture.path), "--issue", "MISSING"]
            )
        self.assertNotEqual(exit_code, 0)
        self.assertIn("unknown requested issue_id: MISSING", errors.getvalue())

    def test_deterministic_json_result_structure(self) -> None:
        first = self.analyze(
            [episode("E2", "2020-01-02", "A"), episode("E1", "2020-01-01", "L")],
            [transition("T1", "E1", "E2")],
        )
        second = json.loads(engine.render_json(first))
        self.assertEqual(first, second)
        self.assertEqual(
            first["metadata"],
            {
                "analysis_code_ref": "test-engine-ref",
                "as_of_date": None,
                "canonical_data_ref": "test-data-ref",
                "derived_protocol_version": "v0.1",
                "engine_version": "v0.1",
            },
        )
        self.assertEqual([node["episode_id"] for node in first["issues"][0]["nodes"]], ["E1", "E2"])
        self.assertEqual(engine.render_json(first), engine.render_json(second))

    def test_issue_with_no_episodes_is_analyzable(self) -> None:
        result = self.analyze([], [])["issues"][0]
        self.assertIsNone(result["lineage_span_days"])
        self.assertEqual(result["weakly_connected_components"], 0)
        self.assertEqual(result["warnings"][0]["code"], "no_canonical_episodes")

    def test_as_of_date_before_start_date_fails(self) -> None:
        with self.assertRaisesRegex(engine.ValidationError, "precedes start_date"):
            self.analyze(
                [episode("E1", "2020-01-01", "L")],
                [],
                as_of_date=date(2019, 12, 31),
            )


if __name__ == "__main__":
    unittest.main()
