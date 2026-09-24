from pathlib import Path
import pytest

from organvm_scrutator.viz.dashboard import Dashboard


def test_export_html_fresh_default_data_dir(tmp_path):
    data_dir = tmp_path / "data_store"
    dashboard = Dashboard(data_dir=str(data_dir))

    expected_path = str(data_dir / "indices" / "dashboard.html")
    returned_path = dashboard.export_html()

    assert returned_path == expected_path
    export_file = Path(returned_path)
    assert export_file.is_file()
    assert export_file.stat().st_size > 0
    assert "ORGANVM Scrutator Dashboard" in export_file.read_text()


def test_export_html_bare_relative_filename(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    dashboard = Dashboard()

    filename = "bare_dashboard.html"
    returned_path = dashboard.export_html(filename)

    assert returned_path == filename
    export_file = Path(filename)
    assert export_file.is_file()
    assert export_file.stat().st_size > 0
    assert "ORGANVM Scrutator Dashboard" in export_file.read_text()


def test_export_html_nested_relative_path(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    dashboard = Dashboard()

    rel_path = "nested/deep/directory/dashboard.html"
    returned_path = dashboard.export_html(rel_path)

    assert returned_path == rel_path
    export_file = Path(rel_path)
    assert export_file.is_file()
    assert export_file.stat().st_size > 0
    assert "ORGANVM Scrutator Dashboard" in export_file.read_text()


def test_export_html_absolute_path(tmp_path):
    dashboard = Dashboard()
    abs_path = str(tmp_path / "abs_export" / "output.html")

    returned_path = dashboard.export_html(abs_path)

    assert returned_path == abs_path
    export_file = Path(abs_path)
    assert export_file.is_file()
    assert export_file.stat().st_size > 0
    assert "ORGANVM Scrutator Dashboard" in export_file.read_text()


def test_export_html_spaces_and_unicode(tmp_path):
    dashboard = Dashboard()
    unicode_path = str(tmp_path / "dáshboard foldér" / "📊 export 01.html")

    returned_path = dashboard.export_html(unicode_path)

    assert returned_path == unicode_path
    export_file = Path(unicode_path)
    assert export_file.is_file()
    assert export_file.stat().st_size > 0
    assert "ORGANVM Scrutator Dashboard" in export_file.read_text()


def test_export_html_repeated_export(tmp_path):
    dashboard = Dashboard(data_dir=str(tmp_path / "data"))

    first_path = dashboard.export_html()
    assert Path(first_path).is_file()

    second_path = dashboard.export_html()
    assert second_path == first_path
    assert Path(second_path).is_file()


def test_export_html_directory_as_output_fails(tmp_path):
    dashboard = Dashboard()
    dir_path = tmp_path / "output_is_a_dir"
    dir_path.mkdir(parents=True, exist_ok=True)

    with pytest.raises(OSError):
        dashboard.export_html(str(dir_path))


def test_export_html_non_directory_parent_fails(tmp_path):
    dashboard = Dashboard()
    file_as_parent = tmp_path / "regular_file"
    file_as_parent.write_text("i am a file")

    invalid_target = file_as_parent / "dashboard.html"

    with pytest.raises(OSError):
        dashboard.export_html(str(invalid_target))
