import io
import os

import pytest

reportlab = pytest.importorskip("reportlab")

from lat_ces.scientific.analysis.plenum import PlenumAnalysisEngine
from lat_ces.scientific.devices.device import create_pitot_tube
from lat_ces.scientific.dimensions.dimension import LENGTH, MASS, TIME
from lat_ces.scientific.quantity import PhysicalQuantity
from lat_ces.scientific.reports.exporter import SKOReportExporter
from lat_ces.scientific.reports.pdf_generator import SKOPDFGenerator
from lat_ces.scientific.units.units import Unit


def test_pdf_generator_stream():
    """Verifikuje da SKOPDFGenerator uspesno generise netrivijalan PDF u BytesIO stream."""
    pascal = Unit("pascal", "Pa", MASS / (LENGTH * (TIME ** 2)))
    m_s = Unit("meter per second", "m/s", LENGTH / TIME)

    device = create_pitot_tube("Lab Pitot Probe")
    velocity = PhysicalQuantity(18.5, 0.378, m_s)
    calculated_p = PhysicalQuantity(206.04, 8.68, pascal)
    limit_p = PhysicalQuantity(220.0, 0.0, pascal)

    report = PlenumAnalysisEngine.evaluate_limit(calculated_p, limit_p)

    exporter = SKOReportExporter(
        project_name="PDF Test Project",
        engineer_name="fahrudin Susnjar",
        plenum_id="PLENUM-PDF-01",
        safety_report=report,
        inputs={"velocity": velocity},
        device=device,
        equation_name="Dinamicki Pritisak",
    )

    pdf_stream = io.BytesIO()
    SKOPDFGenerator.generate_pdf(exporter, pdf_stream)

    pdf_bytes = pdf_stream.getvalue()
    assert len(pdf_bytes) > 1000
    assert pdf_bytes.startswith(b"%PDF")


def test_pdf_generator_file_output(tmp_path):
    """Verifikuje generisanje PDF fajla na disk."""
    pascal = Unit("pascal", "Pa", MASS / (LENGTH * (TIME ** 2)))
    m_s = Unit("meter per second", "m/s", LENGTH / TIME)

    velocity = PhysicalQuantity(18.5, 0.378, m_s)
    calculated_p = PhysicalQuantity(206.04, 8.68, pascal)
    limit_p = PhysicalQuantity(220.0, 0.0, pascal)

    report = PlenumAnalysisEngine.evaluate_limit(calculated_p, limit_p)

    exporter = SKOReportExporter(
        project_name="Disk PDF Test",
        engineer_name="fahrudin Susnjar",
        plenum_id="PLENUM-DISK-01",
        safety_report=report,
        inputs={"velocity": velocity},
    )

    file_path = os.path.join(tmp_path, "test_report.pdf")
    SKOPDFGenerator.generate_pdf(exporter, file_path)

    assert os.path.exists(file_path)
    assert os.path.getsize(file_path) > 1000
