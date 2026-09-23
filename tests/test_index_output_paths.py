import json

import pytest

from organvm_scrutator.scanner.plan_scanner import PlanScanner


def test_save_index_normal_md_path(tmp_path):
    scanner = PlanScanner()
    output_path = tmp_path / "visibility-index.md"

    returned_path = scanner.save_index(str(output_path))
    assert returned_path == str(output_path)

    md_file = output_path
    json_file = tmp_path / "visibility-index.json"

    assert md_file.exists()
    assert json_file.exists()
    assert md_file != json_file

    md_content = md_file.read_text()
    assert md_content.startswith("# Visibility Index")

    json_data = json.loads(json_file.read_text())
    assert "total_plans" in json_data


def test_save_index_extensionless_path(tmp_path):
    scanner = PlanScanner()
    output_path = tmp_path / "visibility-index"

    returned_path = scanner.save_index(str(output_path))
    assert returned_path == str(output_path)

    md_file = output_path
    json_file = tmp_path / "visibility-index.json"

    assert md_file.exists()
    assert json_file.exists()
    assert md_file != json_file

    md_content = md_file.read_text()
    assert md_content.startswith("# Visibility Index")

    json_data = json.loads(json_file.read_text())
    assert "total_plans" in json_data


def test_save_index_parent_dir_with_md_extension(tmp_path):
    scanner = PlanScanner()
    parent_dir = tmp_path / "subdir.md"
    output_path = parent_dir / "index.md"

    returned_path = scanner.save_index(str(output_path))
    assert returned_path == str(output_path)

    md_file = parent_dir / "index.md"
    json_file = parent_dir / "index.json"

    assert md_file.exists()
    assert json_file.exists()
    assert md_file != json_file

    # Ensure parent dir name is preserved and no weird directory path rewriting happened
    assert md_file.parent.name == "subdir.md"
    assert json_file.parent.name == "subdir.md"

    md_content = md_file.read_text()
    assert md_content.startswith("# Visibility Index")
    json_data = json.loads(json_file.read_text())
    assert "total_plans" in json_data


def test_save_index_parent_dir_with_md_extension_and_extensionless_file(tmp_path):
    scanner = PlanScanner()
    parent_dir = tmp_path / "subdir.md"
    output_path = parent_dir / "visibility"

    returned_path = scanner.save_index(str(output_path))
    assert returned_path == str(output_path)

    md_file = parent_dir / "visibility"
    json_file = parent_dir / "visibility.json"

    assert md_file.exists()
    assert json_file.exists()
    assert md_file != json_file

    md_content = md_file.read_text()
    assert md_content.startswith("# Visibility Index")
    json_data = json.loads(json_file.read_text())
    assert "total_plans" in json_data


def test_save_index_ambiguous_json_path_fails_before_mutation(tmp_path):
    scanner = PlanScanner()
    output_path = tmp_path / "index.json"
    original_content = "initial content"
    output_path.write_text(original_content)

    with pytest.raises(ValueError, match="collide|ambiguous|json"):
        scanner.save_index(str(output_path))

    # Verify file was not mutated
    assert output_path.read_text() == original_content


def test_save_index_preexisting_files(tmp_path):
    scanner = PlanScanner()
    md_file = tmp_path / "index.md"
    json_file = tmp_path / "index.json"

    md_file.write_text("old md")
    json_file.write_text("old json")

    scanner.save_index(str(md_file))

    assert md_file.read_text().startswith("# Visibility Index")
    json_data = json.loads(json_file.read_text())
    assert "total_plans" in json_data
