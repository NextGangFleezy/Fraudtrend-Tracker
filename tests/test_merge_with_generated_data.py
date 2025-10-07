import pytest

pd = pytest.importorskip("pandas")

from utils.custom_data_loader import merge_with_generated_data


def _build_custom_df(count):
    records = []
    for idx in range(count):
        records.append(
            {
                "case_id": f"C{idx:03d}",
                "detection_date": pd.Timestamp("2024-01-01") + pd.Timedelta(days=idx),
                "fraud_type": "Account Takeover",
                "reported_amount": 1000.0 + idx,
                "risk_level": "High",
                "status": "Confirmed",
                "region": "North America",
                "detection_method": "Manual Review",
                "case_summary": f"Case summary {idx}",
                "tags": "tag",
                "analyst_notes": "note",
                "id": idx + 1,
            }
        )
    return pd.DataFrame(records)


def _build_generated_df(count):
    records = []
    for idx in range(count):
        records.append(
            {
                "case_id": f"CASE-{idx:03d}",
                "detection_date": pd.Timestamp("2024-02-01") + pd.Timedelta(days=idx),
                "fraud_type": "Synthetic Identity",
                "reported_amount": 500.0 + idx,
                "risk_level": "Medium",
                "status": "Open",
                "region": "Europe",
                "detection_method": "Automated System",
                "case_summary": f"Generated summary {idx}",
                "id": idx + 1,
            }
        )
    return pd.DataFrame(records)


def _count_custom_rows(df):
    if df.empty:
        return 0
    return (~df["case_id"].str.startswith("GEN-", na=False)).sum()


def test_merge_with_generated_data_clamps_ratio_bounds():
    custom_df = _build_custom_df(3)
    generated_df = _build_generated_df(5)

    merged_zero = merge_with_generated_data(custom_df, generated_df, custom_ratio=-0.5)
    assert len(merged_zero) == len(generated_df)
    assert merged_zero["case_id"].str.startswith("GEN-").all()
    assert list(merged_zero["id"]) == list(range(1, len(merged_zero) + 1))

    merged_all_custom = merge_with_generated_data(custom_df, generated_df, custom_ratio=1.5)
    assert len(merged_all_custom) == len(custom_df)
    assert list(merged_all_custom["case_id"]) == list(custom_df["case_id"])


def test_merge_with_generated_data_targets_ratio_when_possible():
    custom_df = _build_custom_df(10)
    generated_df = _build_generated_df(100)

    merged = merge_with_generated_data(custom_df, generated_df, custom_ratio=0.6)

    total_rows = len(merged)
    custom_rows = _count_custom_rows(merged)
    actual_ratio = custom_rows / total_rows

    assert total_rows == 15
    assert custom_rows == 9
    assert actual_ratio == pytest.approx(0.6, abs=1e-6)


def test_merge_with_generated_data_handles_generated_shortage():
    custom_df = _build_custom_df(2)
    generated_df = _build_generated_df(1)

    merged = merge_with_generated_data(custom_df, generated_df, custom_ratio=0.6)

    custom_rows = _count_custom_rows(merged)
    generated_rows = len(merged) - custom_rows

    assert custom_rows == 2
    assert generated_rows == 1
    assert custom_rows / len(merged) >= 0.6
