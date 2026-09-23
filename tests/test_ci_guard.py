from pathlib import Path

import pytest

from organvm_scrutator.ci_guard import read_total_plans, should_publish_scan


def test_empty_hosted_scan_selects_no_publish_path(tmp_path: Path):
    index = tmp_path / "visibility-index.json"
    index.write_text('{"total_plans": 0}')

    assert read_total_plans(index) == 0
    assert should_publish_scan(index) is False


def test_nonempty_hosted_scan_allows_followups(tmp_path: Path):
    index = tmp_path / "visibility-index.json"
    index.write_text('{"total_plans": 3}')

    assert read_total_plans(index) == 3
    assert should_publish_scan(index) is True


def test_missing_index_is_treated_as_empty(tmp_path: Path):
    index = tmp_path / "missing.json"

    assert read_total_plans(index) == 0
    assert should_publish_scan(index) is False


def test_invalid_plan_count_fails_closed(tmp_path: Path):
    index = tmp_path / "visibility-index.json"
    index.write_text('{"total_plans": "many"}')

    with pytest.raises(ValueError, match="non-negative integer"):
        read_total_plans(index)


def test_non_object_index_fails_with_validation_error(tmp_path: Path):
    index = tmp_path / "visibility-index.json"
    index.write_text('[]')

    with pytest.raises(TypeError, match="non-negative integer"):
        read_total_plans(index)


def test_daily_workflow_guards_all_mutating_followups():
    workflow = Path(__file__).parents[1] / ".github" / "workflows" / "daily-scan.yml"
    text = workflow.read_text()

    assert text.count("if: steps.check_plans.outputs.publish_scan == 'true'") == 2
    assert "if: needs.scan.outputs.publish_scan == 'true'" in text
