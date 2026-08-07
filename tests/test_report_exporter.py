import json

import pytest

from lat_ces.scientific.analysis.plenum import PlenumAnalysisEngine
from lat_ces.scientific.devices.device import create_pitot_tube
from lat_ces.scientific.dimensions.dimension import LENGTH, MASS, TIME
from lat_ces.scientific.quantity import PhysicalQuantity
from lat_ces.scientific.reports.exporter import SKOReportExporter
from lat_ces.scientific.units.units import Unit


def test_report_exporter_json_and_markdown():
    """Verifikuje da SKOReportExporter generise ispravne JSON i Markdown certifikate."""
    pascal = Unit("pascal", "Pa", MASS / (LENGTH * (TIME**2)))
    m_s = Unit("meter per second", "m/s", LENGTH / TIME)

    device = create_pitot_tube("Lab Pitot Probe")
    velocity = PhysicalQuantity(18.5, 0.378, m_s)
    calculated_p = PhysicalQuantity(206.04, 8.68, pascal)
    limit_p = PhysicalQuantity(220.0, 0.0, pascal)

    report = PlenumAnalysisEngine.evaluate_limit(calculated_p, limit_p)

    exporter = SKOReportExporter(
        project_name="LAT-CES Vent Test",
        engineer_name="fahrudin Susnjar",
        plenum_id="PLENUM-NORTH-01",
        safety_report=report,
        inputs={"velocity": velocity},
        device=device,
        equation_name="Dinamicki Pritisak",
    )

    json_str = exporter.to_json()
    data = json.loads(json_str)

    assert data["metadata"]["project_name"] == "LAT-CES Vent Test"
    assert data["evaluation"]["status"] == "METROLOGICAL_RISK"
    assert data["device"]["name"] == "Lab Pitot Probe"

    markdown = exporter.to_markdown()
    assert "# 📜 SKO CERTIFIKAT SIGURNOSTI PLENUMA" in markdown
    assert "METROLOGICAL RISK" in markdown
    assert "206.0400" in markdown