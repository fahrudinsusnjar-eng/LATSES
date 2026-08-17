from lat_ces.catalog.cross_source import CrossSourceStatus, SourceObservation, compare_observations


def test_cross_source_consistent_keeps_manufacturer_primary():
    observations = (
        SourceObservation("mfr", "manufacturer_tds", 780, "kg/m3", "2026-08-16", "https://manufacturer.example/tds", primary=True),
        SourceObservation("lab", "independent_lab", 780, "kg/m3", "2026-08-16", "https://lab.example/report"),
    )
    result = compare_observations("P-1", "density", observations, compared_at="2026-08-16")
    assert result.status is CrossSourceStatus.CONSISTENT
    assert result.primary_source_id == "mfr"


def test_cross_source_discrepancy_is_flagged_not_resolved():
    observations = (
        SourceObservation("mfr", "manufacturer_tds", 780, "kg/m3", "2026-08-16", "https://manufacturer.example/tds", primary=True),
        SourceObservation("catalog", "technical_catalog", 785, "kg/m3", "2026-08-16", "https://catalog.example/item"),
    )
    result = compare_observations("P-1", "density", observations, compared_at="2026-08-16")
    assert result.status is CrossSourceStatus.DISCREPANT
    assert result.observations[0].value == 780
    assert result.observations[1].value == 785


def test_cross_source_requires_one_primary_manufacturer_observation():
    observations = (
        SourceObservation("lab", "independent_lab", 780, "kg/m3", "2026-08-16", "https://lab.example/report"),
    )
    try:
        compare_observations("P-1", "density", observations, compared_at="2026-08-16")
    except ValueError:
        return
    raise AssertionError("manufacturer primary observation is required")
