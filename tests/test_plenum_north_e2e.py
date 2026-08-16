"""End-to-end regression test for the canonical LAT-CES plenum example."""

import json
from pathlib import Path

from lat_ces.application.service import analyze_config, export_report, load_config


REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = REPO_ROOT / "examples" / "plenum_north_config.json"
REFERENCE_REPORT_PATH = REPO_ROOT / "examples" / "plenum_north_report.json"


def test_plenum_north_config_to_report_integrity(tmp_path):
    """Verify the canonical config reproduces the canonical safety result."""
    config = load_config(CONFIG_PATH)
    reference = json.loads(REFERENCE_REPORT_PATH.read_text(encoding="utf-8"))

    report, exporter = analyze_config(
        config,
        project_default="LAT-CES CLI Analysis",
        plenum_default="PLENUM-CLI-01",
        equation_default="Custom equation",
    )
    output = export_report(exporter, tmp_path / "plenum_north.json", "json")
    generated = json.loads(output.read_text(encoding="utf-8"))

    assert generated["evaluation"]["status"] == reference["evaluation"]["status"]
    assert generated["evaluation"]["calculated_value"] == reference["evaluation"]["calculated_value"]
    assert generated["evaluation"]["limit_value"] == reference["evaluation"]["limit_value"]
    assert generated["evaluation"]["coverage_factor_k"] == reference["evaluation"]["coverage_factor_k"]
    assert generated["evaluation"]["expanded_uncertainty"] == reference["evaluation"]["expanded_uncertainty"]
    assert generated["evaluation"]["margin_to_limit"] == reference["evaluation"]["margin_to_limit"]
    assert generated["metadata"]["project_name"] == config["project_name"]
    assert generated["metadata"]["plenum_id"] == config["plenum_id"]
    assert report.status.value == reference["evaluation"]["status"]
