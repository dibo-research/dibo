"""Tests for the DIBO Evidence Reliability Pilot Kit."""

from __future__ import annotations

import csv
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


sys.path.insert(0, str(Path(__file__).resolve().parent))
import pilot  # noqa: E402


class PilotTests(unittest.TestCase):
    def setUp(self) -> None:
        self.git_verification = mock.patch.object(pilot, "verify_canonical_checkout")
        self.git_verification.start()
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.data = self.root / "data"
        self.data.mkdir()
        self.scope_path = self.root / "scope.json"
        self._write_csv(
            self.data / "issues.csv",
            ["issue_id", "title"],
            [["SYN-ISSUE", "Synthetic issue"], ["OTHER-ISSUE", "Other issue"]],
        )
        self._write_csv(
            self.data / "episodes.csv",
            ["episode_id", "issue_id"],
            [
                ["SYN-E02", "SYN-ISSUE"],
                ["SYN-E01", "SYN-ISSUE"],
                ["OTHER-E01", "OTHER-ISSUE"],
            ],
        )
        self._write_csv(
            self.data / "transitions.csv",
            ["transition_id", "issue_id"],
            [
                ["SYN-T02", "SYN-ISSUE"],
                ["SYN-T01", "SYN-ISSUE"],
                ["OTHER-T01", "OTHER-ISSUE"],
            ],
        )
        self.scope = {
            "scope_id": "SCOPE-SYN",
            "issue_id": "SYN-ISSUE",
            "tracked_matter": "Whether the synthetic request was handled",
            "included_episode_ids": ["SYN-E02", "SYN-E01"],
            "included_transition_ids": ["SYN-T02", "SYN-T01"],
            "canonical_data_ref": "synthetic-ref",
            "evidence_protocol_version": "v0.1",
        }
        self._write_scope()

    def tearDown(self) -> None:
        self.temp.cleanup()
        self.git_verification.stop()

    @staticmethod
    def _write_csv(path: Path, header: list[str], rows: list[list[str]]) -> None:
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle, lineterminator="\n")
            writer.writerow(header)
            writer.writerows(rows)

    def _write_scope(self) -> None:
        self.scope_path.write_text(json.dumps(self.scope), encoding="utf-8")

    def _generate(self, coder_id: str = "C01", name: str | None = None) -> Path:
        path = self.root / (name or f"{coder_id}.csv")
        pilot.generate_sheet(self.scope_path, coder_id, self.data, path)
        return path

    @staticmethod
    def _read_rows(path: Path) -> list[dict[str, str]]:
        with path.open("r", encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle))

    def _write_rows(self, path: Path, rows: list[dict[str, str]]) -> None:
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(
                handle, fieldnames=pilot.SHEET_HEADER, lineterminator="\n"
            )
            writer.writeheader()
            writer.writerows(rows)

    def _complete(
        self,
        coder_id: str,
        codes: dict[tuple[str, str], str] | None = None,
        name: str | None = None,
    ) -> Path:
        path = self._generate(coder_id, name)
        rows = self._read_rows(path)
        for row in rows:
            row["code"] = (codes or {}).get(
                (row["unit_id"], row["concept"]), "YES"
            )
            row["source_ref"] = "synthetic-source"
            row["source_locator"] = ""
            row["rationale"] = "Synthetic rationale."
        self._write_rows(path, rows)
        return path

    def _assert_invalid(self, path: Path, pattern: str | None = None) -> None:
        context = self.assertRaises(pilot.PilotError)
        with context:
            pilot.validate_completed_sheet(self.scope_path, path, self.data)
        if pattern is not None:
            self.assertIn(pattern, str(context.exception))

    def test_deterministic_generation(self) -> None:
        first = self._generate(name="first.csv")
        second = self._generate(name="second.csv")
        self.assertEqual(first.read_bytes(), second.read_bytes())

    def test_expected_e_plus_three_t_row_count(self) -> None:
        self.assertEqual(len(self._read_rows(self._generate())), 2 + (3 * 2))

    def test_episode_maps_to_substantive_disposition(self) -> None:
        rows = self._read_rows(self._generate())
        episode_rows = [row for row in rows if row["unit_type"] == "EPISODE"]
        self.assertEqual(
            {row["concept"] for row in episode_rows}, {"SUBSTANTIVE_DISPOSITION"}
        )

    def test_transition_maps_to_exactly_three_concepts(self) -> None:
        rows = self._read_rows(self._generate())
        concepts = [
            row["concept"] for row in rows if row["unit_id"] == "SYN-T01"
        ]
        self.assertEqual(concepts, pilot.TRANSITION_CONCEPTS)

    def test_deterministic_unit_and_concept_order(self) -> None:
        rows = self._read_rows(self._generate())
        actual = [(row["unit_id"], row["concept"]) for row in rows]
        expected = [
            ("SYN-E01", "SUBSTANTIVE_DISPOSITION"),
            ("SYN-E02", "SUBSTANTIVE_DISPOSITION"),
            *[("SYN-T01", concept) for concept in pilot.TRANSITION_CONCEPTS],
            *[("SYN-T02", concept) for concept in pilot.TRANSITION_CONCEPTS],
        ]
        self.assertEqual(actual, expected)

    def test_generated_evidence_fields_are_blank(self) -> None:
        rows = self._read_rows(self._generate())
        self.assertTrue(
            all(
                row[field] == ""
                for row in rows
                for field in ["code", "source_ref", "source_locator", "rationale"]
            )
        )

    def test_duplicate_included_episode_rejected(self) -> None:
        self.scope["included_episode_ids"] = ["SYN-E01", "SYN-E01"]
        self._write_scope()
        with self.assertRaisesRegex(pilot.PilotError, "duplicate included Episode"):
            self._generate()

    def test_duplicate_included_transition_rejected(self) -> None:
        self.scope["included_transition_ids"] = ["SYN-T01", "SYN-T01"]
        self._write_scope()
        with self.assertRaisesRegex(pilot.PilotError, "duplicate included Transition"):
            self._generate()

    def test_unknown_issue_rejected(self) -> None:
        self.scope["issue_id"] = "MISSING-ISSUE"
        self._write_scope()
        with self.assertRaisesRegex(pilot.PilotError, "unknown issue_id"):
            self._generate()

    def test_unknown_episode_rejected(self) -> None:
        self.scope["included_episode_ids"] = ["MISSING-E"]
        self._write_scope()
        with self.assertRaisesRegex(pilot.PilotError, "unknown included Episode"):
            self._generate()

    def test_unknown_transition_rejected(self) -> None:
        self.scope["included_transition_ids"] = ["MISSING-T"]
        self._write_scope()
        with self.assertRaisesRegex(pilot.PilotError, "unknown included Transition"):
            self._generate()

    def test_wrong_issue_episode_rejected(self) -> None:
        self.scope["included_episode_ids"] = ["OTHER-E01"]
        self._write_scope()
        with self.assertRaisesRegex(pilot.PilotError, "belongs to issue_id OTHER-ISSUE"):
            self._generate()

    def test_wrong_issue_transition_rejected(self) -> None:
        self.scope["included_transition_ids"] = ["OTHER-T01"]
        self._write_scope()
        with self.assertRaisesRegex(pilot.PilotError, "belongs to issue_id OTHER-ISSUE"):
            self._generate()

    def test_unfilled_scope_template_rejected(self) -> None:
        self.scope["scope_id"] = ""
        self._write_scope()
        with self.assertRaisesRegex(pilot.PilotError, "scope_id"):
            self._generate()

    def test_wrong_protocol_version_rejected(self) -> None:
        self.scope["evidence_protocol_version"] = "v9.9"
        self._write_scope()
        with self.assertRaisesRegex(pilot.PilotError, "must be v0.1"):
            self._generate()

    def test_blank_coder_id_rejected(self) -> None:
        with self.assertRaisesRegex(pilot.PilotError, "coder_id must be non-empty"):
            self._generate(coder_id=" ")

    def test_generate_cannot_overwrite_scope_or_canonical_files(self) -> None:
        protected = [
            self.scope_path,
            self.data / "issues.csv",
            self.data / "episodes.csv",
            self.data / "transitions.csv",
        ]
        before = {path: path.read_bytes() for path in protected}
        for path in protected:
            with self.subTest(path=path.name):
                with self.assertRaisesRegex(pilot.PilotError, "protected input"):
                    pilot.generate_sheet(self.scope_path, "C01", self.data, path)
        self.assertEqual(before, {path: path.read_bytes() for path in protected})

    def test_generate_protection_uses_resolved_paths(self) -> None:
        scope_alias = self.data / ".." / self.scope_path.name
        before = self.scope_path.read_bytes()
        with self.assertRaisesRegex(pilot.PilotError, "protected input"):
            pilot.generate_sheet(self.scope_path, "C01", self.data, scope_alias)
        self.assertEqual(self.scope_path.read_bytes(), before)

    def test_generate_replaces_an_unprotected_output(self) -> None:
        output = self.root / "ordinary-output.csv"
        output.write_text("stale", encoding="utf-8")
        pilot.generate_sheet(self.scope_path, "C01", self.data, output)
        self.assertEqual(len(self._read_rows(output)), 2 + (3 * 2))

    def test_completed_valid_sheet_passes(self) -> None:
        result = pilot.validate_completed_sheet(
            self.scope_path, self._complete("C01"), self.data
        )
        self.assertEqual(result.coder_id, "C01")

    def test_blank_source_locator_is_allowed(self) -> None:
        pilot.validate_completed_sheet(self.scope_path, self._complete("C01"), self.data)

    def test_wrong_header_fails(self) -> None:
        path = self._complete("C01")
        text = path.read_text(encoding="utf-8").replace("scope_id", "scope", 1)
        path.write_text(text, encoding="utf-8")
        self._assert_invalid(path, "header")

    def test_short_malformed_row_fails_closed(self) -> None:
        path = self._complete("C01")
        lines = path.read_text(encoding="utf-8").splitlines()
        lines[1] = "SCOPE-SYN,C01,EPISODE"
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        self._assert_invalid(path, "malformed row")

    def test_missing_expected_pair_fails(self) -> None:
        path = self._complete("C01")
        rows = self._read_rows(path)
        self._write_rows(path, rows[:-1])
        self._assert_invalid(path, "missing unit-concept pair")

    def test_duplicate_unit_concept_pair_fails(self) -> None:
        path = self._complete("C01")
        rows = self._read_rows(path)
        rows[-1] = rows[0].copy()
        self._write_rows(path, rows)
        self._assert_invalid(path, "duplicate unit-concept pair")

    def test_extra_unit_concept_pair_fails(self) -> None:
        path = self._complete("C01")
        rows = self._read_rows(path)
        extra = rows[0].copy()
        extra["unit_id"] = "OUTSIDE-E"
        rows.append(extra)
        self._write_rows(path, rows)
        self._assert_invalid(path, "outside the frozen scope")

    def test_invalid_categorical_code_fails(self) -> None:
        path = self._complete("C01")
        rows = self._read_rows(path)
        rows[0]["code"] = "MAYBE"
        self._write_rows(path, rows)
        self._assert_invalid(path, "invalid categorical code")

    def test_blank_categorical_code_fails(self) -> None:
        path = self._complete("C01")
        rows = self._read_rows(path)
        rows[0]["code"] = ""
        self._write_rows(path, rows)
        self._assert_invalid(path, "blank code")

    def test_blank_rationale_fails(self) -> None:
        path = self._complete("C01")
        rows = self._read_rows(path)
        rows[0]["rationale"] = " "
        self._write_rows(path, rows)
        self._assert_invalid(path, "blank rationale")

    def test_multiple_coder_ids_in_one_sheet_fail(self) -> None:
        path = self._complete("C01")
        rows = self._read_rows(path)
        rows[0]["coder_id"] = "C02"
        self._write_rows(path, rows)
        self._assert_invalid(path, "exactly one coder_id")

    def test_same_coder_for_both_sheets_fails(self) -> None:
        first = self._complete("C01", name="first.csv")
        second = self._complete("C01", name="second.csv")
        with self.assertRaisesRegex(pilot.PilotError, "different coder IDs"):
            pilot.calculate_reliability(self.scope_path, first, second, self.data)

    def test_exact_agreement_calculation(self) -> None:
        first = self._complete("C01")
        second = self._complete(
            "C02", {("SYN-E02", "SUBSTANTIVE_DISPOSITION"): "NO"}
        )
        result = pilot.calculate_reliability(self.scope_path, first, second, self.data)
        concept = result["concepts"]["SUBSTANTIVE_DISPOSITION"]
        self.assertEqual(concept["agreement_count"], 1)
        self.assertEqual(concept["exact_agreement_proportion"], 0.5)

    def test_disagreement_count_and_list(self) -> None:
        first = self._complete("C01")
        second = self._complete(
            "C02", {("SYN-T02", "DOCUMENTED_REDIRECTION"): "NO"}
        )
        result = pilot.calculate_reliability(self.scope_path, first, second, self.data)
        concept = result["concepts"]["DOCUMENTED_REDIRECTION"]
        self.assertEqual(concept["disagreement_count"], 1)
        self.assertEqual(concept["disagreements"][0]["unit_id"], "SYN-T02")
        self.assertNotIn("rationale", concept["disagreements"][0])

    def test_code_distributions_include_all_codes(self) -> None:
        first = self._complete(
            "C01", {("SYN-E02", "SUBSTANTIVE_DISPOSITION"): "NO"}
        )
        second = self._complete(
            "C02", {("SYN-E02", "SUBSTANTIVE_DISPOSITION"): "INDETERMINATE"}
        )
        result = pilot.calculate_reliability(self.scope_path, first, second, self.data)
        distributions = result["concepts"]["SUBSTANTIVE_DISPOSITION"][
            "code_distribution_by_coder"
        ]
        self.assertEqual(distributions["C01"], {"YES": 1, "NO": 1, "INDETERMINATE": 0})
        self.assertEqual(distributions["C02"], {"YES": 1, "NO": 0, "INDETERMINATE": 1})

    def test_known_calculable_cohen_kappa(self) -> None:
        self.scope["included_episode_ids"] = [f"SYN-E{i:02d}" for i in range(1, 6)]
        self._write_scope()
        self._write_csv(
            self.data / "episodes.csv",
            ["episode_id", "issue_id"],
            [[f"SYN-E{i:02d}", "SYN-ISSUE"] for i in range(1, 6)],
        )
        c1 = {
            ("SYN-E01", "SUBSTANTIVE_DISPOSITION"): "YES",
            ("SYN-E02", "SUBSTANTIVE_DISPOSITION"): "YES",
            ("SYN-E03", "SUBSTANTIVE_DISPOSITION"): "YES",
            ("SYN-E04", "SUBSTANTIVE_DISPOSITION"): "NO",
            ("SYN-E05", "SUBSTANTIVE_DISPOSITION"): "NO",
        }
        c2 = {
            ("SYN-E01", "SUBSTANTIVE_DISPOSITION"): "YES",
            ("SYN-E02", "SUBSTANTIVE_DISPOSITION"): "YES",
            ("SYN-E03", "SUBSTANTIVE_DISPOSITION"): "NO",
            ("SYN-E04", "SUBSTANTIVE_DISPOSITION"): "NO",
            ("SYN-E05", "SUBSTANTIVE_DISPOSITION"): "NO",
        }
        report = pilot.calculate_reliability(
            self.scope_path, self._complete("C01", c1), self._complete("C02", c2), self.data
        )
        result = report["concepts"]["SUBSTANTIVE_DISPOSITION"]
        self.assertEqual(result["cohen_kappa"], 0.615385)
        self.assertEqual(result["cohen_kappa_status"], "CALCULATED")

    def test_kappa_undefined_when_expected_denominator_is_zero(self) -> None:
        result = pilot.calculate_reliability(
            self.scope_path, self._complete("C01"), self._complete("C02"), self.data
        )["concepts"]["SUBSTANTIVE_DISPOSITION"]
        self.assertIsNone(result["cohen_kappa"])
        self.assertEqual(
            result["cohen_kappa_status"], "UNDEFINED_EXPECTED_AGREEMENT"
        )

    def test_zero_unit_concept_has_null_agreement_and_kappa(self) -> None:
        self.scope["included_episode_ids"] = []
        self._write_scope()
        result = pilot.calculate_reliability(
            self.scope_path, self._complete("C01"), self._complete("C02"), self.data
        )["concepts"]["SUBSTANTIVE_DISPOSITION"]
        self.assertEqual(result["coding_unit_count"], 0)
        self.assertIsNone(result["exact_agreement_proportion"])
        self.assertIsNone(result["cohen_kappa"])
        self.assertEqual(result["cohen_kappa_status"], "NO_UNITS")

    def test_reliability_output_is_deterministic_and_argument_order_independent(self) -> None:
        first = self._complete("C02")
        second = self._complete("C01")
        forward = pilot.reliability_json(
            pilot.calculate_reliability(self.scope_path, first, second, self.data)
        )
        reverse = pilot.reliability_json(
            pilot.calculate_reliability(self.scope_path, second, first, self.data)
        )
        self.assertEqual(forward, reverse)

    def test_no_pooled_or_global_kappa_appears(self) -> None:
        report = pilot.calculate_reliability(
            self.scope_path, self._complete("C01"), self._complete("C02"), self.data
        )
        self.assertEqual(set(report), {"metadata", "concepts"})
        self.assertNotIn("cohen_kappa", report)

    def test_input_sheets_are_not_modified(self) -> None:
        first = self._complete("C01")
        second = self._complete("C02")
        before = (first.read_bytes(), second.read_bytes())
        pilot.calculate_reliability(self.scope_path, first, second, self.data)
        self.assertEqual(before, (first.read_bytes(), second.read_bytes()))

    def test_reliability_cannot_overwrite_scope_sheets_or_canonical_files(self) -> None:
        first = self._complete("C01")
        second = self._complete("C02")
        protected = [
            self.scope_path,
            first,
            second,
            self.data / "issues.csv",
            self.data / "episodes.csv",
            self.data / "transitions.csv",
        ]
        before = {path: path.read_bytes() for path in protected}
        for path in protected:
            with self.subTest(path=path.name):
                stderr = io.StringIO()
                with mock.patch.object(sys, "stderr", stderr):
                    status = pilot.main(
                        [
                            "reliability",
                            "--scope",
                            str(self.scope_path),
                            "--sheet-a",
                            str(first),
                            "--sheet-b",
                            str(second),
                            "--data-dir",
                            str(self.data),
                            "--output",
                            str(path),
                        ]
                    )
                self.assertEqual(status, 1)
                self.assertIn("protected input", stderr.getvalue())
        self.assertEqual(before, {path: path.read_bytes() for path in protected})

    def test_reliability_replaces_an_unprotected_output(self) -> None:
        first = self._complete("C01")
        second = self._complete("C02")
        output = self.root / "ordinary-output.json"
        output.write_text("stale", encoding="utf-8")
        status = pilot.main(
            [
                "reliability",
                "--scope",
                str(self.scope_path),
                "--sheet-a",
                str(first),
                "--sheet-b",
                str(second),
                "--data-dir",
                str(self.data),
                "--output",
                str(output),
            ]
        )
        self.assertEqual(status, 0)
        report = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(report["metadata"]["scope_id"], "SCOPE-SYN")

    def test_cli_invalid_input_does_not_write_output(self) -> None:
        self.scope["scope_id"] = ""
        self._write_scope()
        output = self.root / "must-not-exist.csv"
        stderr = io.StringIO()
        original_stderr = sys.stderr
        try:
            sys.stderr = stderr
            status = pilot.main(
                [
                    "generate",
                    "--scope",
                    str(self.scope_path),
                    "--coder-id",
                    "C01",
                    "--data-dir",
                    str(self.data),
                    "--output",
                    str(output),
                ]
            )
        finally:
            sys.stderr = original_stderr
        self.assertEqual(status, 1)
        self.assertFalse(output.exists())
        self.assertTrue(stderr.getvalue().startswith("error:"))


class GitVerificationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.checkout = Path(self.temp.name) / "checkout"
        self.data = self.checkout / "data"
        self.data.mkdir(parents=True)
        self.scope = pilot.Scope(
            scope_id="SCOPE-SYN",
            issue_id="SYN-ISSUE",
            tracked_matter="Synthetic tracked matter",
            included_episode_ids=(),
            included_transition_ids=(),
            canonical_data_ref="a" * 40,
            evidence_protocol_version="v0.1",
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    @staticmethod
    def _result(returncode: int = 0, stdout: str = "") -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess([], returncode, stdout=stdout, stderr="")

    def test_git_unavailable_allows_non_git_fixture(self) -> None:
        with mock.patch.object(pilot, "_run_git", return_value=None):
            pilot.verify_canonical_checkout(self.scope, self.data)

    def test_non_git_fixture_skips_git_verification(self) -> None:
        with mock.patch.object(
            pilot, "_run_git", return_value=self._result(returncode=128)
        ):
            pilot.verify_canonical_checkout(self.scope, self.data)

    def test_git_head_mismatch_fails_closed(self) -> None:
        responses = [
            self._result(stdout=str(self.checkout)),
            self._result(stdout="b" * 40 + "\n"),
        ]
        with mock.patch.object(pilot, "_run_git", side_effect=responses):
            with self.assertRaisesRegex(pilot.PilotError, "does not match"):
                pilot.verify_canonical_checkout(self.scope, self.data)

    def test_dirty_canonical_files_fail_closed(self) -> None:
        tracked = "\n".join(
            f"data/{filename}" for filename in pilot.CANONICAL_FILENAMES
        )
        responses = [
            self._result(stdout=str(self.checkout)),
            self._result(stdout="a" * 40 + "\n"),
            self._result(stdout=tracked + "\n"),
            self._result(stdout=" M data/issues.csv\n"),
        ]
        with mock.patch.object(pilot, "_run_git", side_effect=responses):
            with self.assertRaisesRegex(pilot.PilotError, "dirty"):
                pilot.verify_canonical_checkout(self.scope, self.data)

    def test_untracked_canonical_file_fails_closed(self) -> None:
        tracked = "\n".join(
            f"data/{filename}" for filename in pilot.CANONICAL_FILENAMES[:-1]
        )
        responses = [
            self._result(stdout=str(self.checkout)),
            self._result(stdout="a" * 40 + "\n"),
            self._result(stdout=tracked + "\n"),
        ]
        with mock.patch.object(pilot, "_run_git", side_effect=responses):
            with self.assertRaisesRegex(pilot.PilotError, "not tracked"):
                pilot.verify_canonical_checkout(self.scope, self.data)

    def test_matching_clean_git_checkout_passes(self) -> None:
        tracked = "\n".join(
            f"data/{filename}" for filename in pilot.CANONICAL_FILENAMES
        )
        responses = [
            self._result(stdout=str(self.checkout)),
            self._result(stdout="a" * 40 + "\n"),
            self._result(stdout=tracked + "\n"),
            self._result(stdout=""),
        ]
        with mock.patch.object(pilot, "_run_git", side_effect=responses):
            pilot.verify_canonical_checkout(self.scope, self.data)


if __name__ == "__main__":
    unittest.main()
