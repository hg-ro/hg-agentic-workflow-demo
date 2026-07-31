import pytest

from reconciliation import reconcile_csv


def write_csv(tmp_path, text):
    path = tmp_path / "line_items.csv"
    path.write_text(text)
    return str(path)


def test_all_rows_reconcile(tmp_path):
    csv_text = (
        "id,computed,invoiced\n"
        "1,100.00,100.00\n"
        "2,250.50,250.505\n"
    )
    path = write_csv(tmp_path, csv_text)

    result = reconcile_csv(path)

    assert result["reconciled"] == 2
    assert result["flagged"] == 0
    assert result["details"] == []


def test_some_rows_flagged(tmp_path):
    csv_text = (
        "id,computed,invoiced\n"
        "1,100.00,100.00\n"
        "2,500.00,450.00\n"
    )
    path = write_csv(tmp_path, csv_text)

    result = reconcile_csv(path)

    assert result["reconciled"] == 1
    assert result["flagged"] == 1
    assert result["details"] == [
        {"id": "2", "computed": 500.00, "invoiced": 450.00, "gap": pytest.approx(50.00), "error": None}
    ]


def test_boundary_at_tolerance_row_is_reconciled(tmp_path):
    csv_text = (
        "id,computed,invoiced\n"
        "1,500.00,499.99\n"
    )
    path = write_csv(tmp_path, csv_text)

    result = reconcile_csv(path, tolerance=0.01)

    assert result["reconciled"] == 1
    assert result["flagged"] == 0
    assert result["details"] == []


def test_negative_gap_row_is_flagged(tmp_path):
    csv_text = (
        "id,computed,invoiced\n"
        "1,500.00,500.05\n"
    )
    path = write_csv(tmp_path, csv_text)

    result = reconcile_csv(path, tolerance=0.01)

    assert result["reconciled"] == 0
    assert result["flagged"] == 1
    detail = result["details"][0]
    assert detail["id"] == "1"
    assert detail["gap"] == pytest.approx(-0.05)
    assert detail["error"] is None


def test_empty_file_header_only(tmp_path):
    csv_text = "id,computed,invoiced\n"
    path = write_csv(tmp_path, csv_text)

    result = reconcile_csv(path)

    assert result["reconciled"] == 0
    assert result["flagged"] == 0
    assert result["details"] == []


def test_row_with_missing_column_is_flagged_as_error(tmp_path):
    # row 2 only has id and computed -- invoiced is entirely absent
    csv_text = (
        "id,computed,invoiced\n"
        "1,100.00,100.00\n"
        "2,100.00\n"
    )
    path = write_csv(tmp_path, csv_text)

    result = reconcile_csv(path)

    assert result["reconciled"] == 1
    assert result["flagged"] == 1
    detail = result["details"][0]
    assert detail["id"] == "2"
    assert detail["gap"] is None
    assert detail["error"] is not None


def test_row_with_non_numeric_amount_is_flagged_as_error(tmp_path):
    csv_text = (
        "id,computed,invoiced\n"
        "1,100.00,100.00\n"
        "2,100.00,N/A\n"
    )
    path = write_csv(tmp_path, csv_text)

    result = reconcile_csv(path)

    assert result["reconciled"] == 1
    assert result["flagged"] == 1
    detail = result["details"][0]
    assert detail["id"] == "2"
    assert detail["gap"] is None
    assert detail["error"] is not None
