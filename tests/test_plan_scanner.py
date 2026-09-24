import pytest
from pathlib import Path
from organvm_scrutator.scanner.plan_scanner import PlanScanner, PlanMetadata


class TestPlanScanner:
    """Tests for the PlanScanner module"""
    
    def test_scanner_initialization(self):
        scanner = PlanScanner()
        assert scanner.workspace_root == scanner.workspace_root
        assert scanner.plans == []
    
    def test_is_excluded(self):
        scanner = PlanScanner()
        assert scanner._is_excluded('contrib--some-repo') == True
        assert scanner._is_excluded('bench/some-repo') == True
        assert scanner._is_excluded('normal-repo') == False
    
    def test_plan_metadata_to_dict(self):
        plan = PlanMetadata(
            plan_id="TEST-001",
            file_path="/test/path.md",
            repo="test-repo",
            created="2026-04-26",
            modified="2026-04-26",
            status="DRAFT"
        )
        d = plan.to_dict()
        assert d['plan_id'] == "TEST-001"
        assert d['repo'] == "test-repo"
        assert d['status'] == "DRAFT"

    def test_scan_directory_skips_matching_directories(self, tmp_path, capsys):
        """Ensure _scan_directory skips directories ending in .md without warning."""
        plan_dir = tmp_path / "plans"
        plan_dir.mkdir()

        valid_plan = plan_dir / "valid_plan.md"
        valid_plan.write_text("**Plan ID:** PLAN-001\n**Status:** ACTIVE\n")

        dir_ending_in_md = plan_dir / "directory.md"
        dir_ending_in_md.mkdir()

        control_txt = plan_dir / "control.txt"
        control_txt.write_text("Not a markdown plan file.")

        scanner = PlanScanner()
        plans = scanner._scan_directory(plan_dir, repo="test-repo")

        assert len(plans) == 1
        assert plans[0].plan_id == "PLAN-001"
        assert plans[0].file_path == str(valid_plan)

        captured = capsys.readouterr()
        assert captured.out == ""
        assert captured.err == ""