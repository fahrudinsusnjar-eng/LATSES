import json

from lat_ces.scientific.analysis import SKOReportExporter
from lat_ces.scientific.analysis.plenum import SafetyReport, SafetyStatus
from lat_ces.scientific.devices.device import create_pitot_tube
from lat_ces.scientific.dimensions.dimension import LENGTH, MASS, TIME
from lat_ces.scientific.quantities.quantity import PhysicalQuantity
from lat_ces.scientific.units.units import Unit


def _make_context():
    pascal = Unit("pascal", "Pa", MASS / (LENGTH * (TIME**2)))
    velocity_unit = Unit("meter per second", "m/s", LENGTH / TIME)
    velocity = PhysicalQuantity(18.5, 0.3775, velocity_unit)
    pressure = PhysicalQuantity(206.04, 8.68, pascal)
    limit = PhysicalQuantity(220.0, 0.0, pascal)
    report = SafetyReport(
        status=SafetyStatus.METROLOGICAL_RISK,
        calculated_value=pressure,
        limit_value=limit,
        expanded_uncertainty=17.36,
        coverage_factor=2.0,
        margin_to_limit=13.96,
        message="UPOZORENJE (METROLOSKI RIZIK)",
    )
    return velocity, report


def test_sko_report_exporter_to_dict_and_json():
    velocity, report = _make_context()
    exporter = SKOReportExporter(
        project_name="LAT Demo",
        engineer_name="Engineer",
        plenum_id="PL-001",
        safety_report=report,
        inputs={"velocity": velocity},
        device=create_pitot_tube(),
        equation_name="Dynamic pressure",
    )

    as_dict = exporter.to_dict()
    assert as_dict["metadata"]["project_name"] == "LAT Demo"
    assert as_dict["evaluation"]["status"] == "METROLOGICAL_RISK"
    assert as_dict["inputs"]["velocity"]["unit_symbol"] == "m/s"
    assert as_dict["device"]["device_type"] == "Pitot Tube"

    as_json = exporter.to_json()
    payload = json.loads(as_json)
    assert payload["equation"] == "Dynamic pressure"
    assert payload["evaluation"]["margin_to_limit"] == 13.96


def test_sko_report_exporter_markdown_contains_core_sections():
    velocity, report = _make_context()
    exporter = SKOReportExporter(
        project_name="LAT Demo",
        engineer_name="Engineer",
        plenum_id="PL-001",
        safety_report=report,
        inputs={"velocity": velocity},
        device=None,
    )

    markdown = exporter.to_markdown()
    assert "SKO CERTIFIKAT SIGURNOSTI PLENUMA" in markdown
    assert "## 1. STATUS EVALUACIJE" in markdown
    assert "METROLOGICAL RISK" in markdown
    assert "Ulaz (velocity)" in markdown