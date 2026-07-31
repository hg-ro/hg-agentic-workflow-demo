import pytest

from reconciliation import reconcile


def test_exact_match_reconciled():
    verdict, gap = reconcile(computed=500.00, invoiced=500.00)
    assert verdict == "RECONCILED"
    assert gap == pytest.approx(0.0)


def test_difference_just_under_tolerance_reconciled():
    # |diff| = 0.0099, tolerance = 0.01 -> within tolerance
    verdict, gap = reconcile(computed=500.00, invoiced=499.9901, tolerance=0.01)
    assert verdict == "RECONCILED"
    assert gap == pytest.approx(0.0099)


def test_difference_equal_to_tolerance_reconciled():
    # |diff| = 0.01, tolerance = 0.01 -> boundary is inclusive
    verdict, gap = reconcile(computed=500.00, invoiced=499.99, tolerance=0.01)
    assert verdict == "RECONCILED"
    assert gap == pytest.approx(0.01)


def test_difference_just_over_tolerance_is_discrepancy():
    # |diff| = 0.0101, tolerance = 0.01 -> outside tolerance
    verdict, gap = reconcile(computed=500.00, invoiced=499.9899, tolerance=0.01)
    assert verdict == "DISCREPANCY"
    assert gap == pytest.approx(0.0101)


def test_invoiced_exceeds_computed_gives_negative_gap():
    verdict, gap = reconcile(computed=500.00, invoiced=500.05, tolerance=0.01)
    assert verdict == "DISCREPANCY"
    assert gap == pytest.approx(-0.05)
