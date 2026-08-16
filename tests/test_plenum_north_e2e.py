"""End-to-end regression test for the canonical LAT-CES plenum example."""

import json
from pathlib import Path

from lat_ces.scientific.analysis.plenum import PlenumAnalysisEngine
from lat_ces.scientific.cli import _parse_quantity_dict
from lat_ces.scientific.reports.exporter import SKOReportExporter


REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = REPO_ROOT / "examples" / "plenum_north_config.json"
REFERENCE_REPORT_PATH = REPO_ROOT / "examples" / "plenum_north_report.json"


def test_plenum_north_config_to_report_integrity():
    """Verify the canonical config reproduces the canonical safety result."""
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    reference = json.loads(REFERENCE_REPORT_PATH.read_text(encoding="utf-8"))

    inputs = {
        name: _parse_quantity_dict(quantity)
        for name, quantity in config.get("inputs", {}).items()
    }
    calculated = _parse_quantity_dict(config["calculated_value"])
    limit = _parse_quantity_dict(config["limit_value"])

    report = PlenumAnalysisEngine.evaluate_limit(
        calculated=calculated,
        limit=limit,
        coverage_factor=float(config.get("coverage_factor", 2.0)),
    )

    exporter = SKOReportExporter(
        project_name=config["project_name"],
        engineer_name=config["engineer_name"],
        plenum_id=config["plenum_id"],
        safety_report=report,
        inputs=inputs,
        equation_name=config.get("equation_name"),
    )
    generated = json.loads(exporter.to_json())

    assert generated["evaluation"]["status"] == reference["evaluation"]["status"]
    assert generated["evaluation"]["calculated_value"] == reference["evaluation"]["calculated_value"]
    assert generated["evaluation"]["limit_value"] == reference["evaluation"]["limit_value"]
    assert generated["evaluation"]["coverage_factor_k"] == reference["evaluation"]["coverage_factor_k"]
    assert generated["evaluation"]["expanded_uncertainty"] == reference["evaluation"]["expanded_uncertainty"]
    assert generated["evaluation"]["margin_to_limit"] == reference["evaluation"]["margin_to_limit"]

    assert generated["metadata"]["project_name"] == config["project_name"]
    assert generated["metadata"]["plenum_id"] == config["plenum_id"]
