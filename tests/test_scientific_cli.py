import json
from pathlib import Path

import pytest

from lat_ces.cli import run_cli


def _write_config(path: Path):
    payload = {
        "project_name": "LAT-CES Vent Test",
        "engineer_name": "fahrudin Susnjar",
        "plenum_id": "PLENUM-NORTH-01",
        "equation_name": "Dinamicki Pritisak",
        "coverage_factor": 2.0,
        "inputs": {
            "velocity": {
                "value": 18.5,
                "uncertainty": 0.378,
                "unit_symbol": "m/s",
            },
            "density": {
                "value": 1.204,
                "uncertainty": 0.012,
                "unit_symbol": "kg/m3",
            },
        },
        "calculated_value": {
            "value": 206.04,
            "uncertainty": 8.68,
            "unit_symbol": "Pa",
        },
        "limit_value": {
            "value": 220.0,
            "uncertainty": 0.0,
            "unit_symbol": "Pa",
        },
    }
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_cli_analyze_json_output(tmp_path):
    config = tmp_path / "config.json"
    report = tmp_path / "report.json"
    _write_config(config)

    code = run_cli(["analyze", "-c", str(config), "-f", "json", "-o", str(report)])

    assert code == 0
    assert report.exists()
    payload = json.loads(report.read_text(encoding="utf-8"))
    assert payload["evaluation"]["status"] == "METROLOGICAL_RISK"


def test_cli_analyze_markdown_output(tmp_path):
    config = tmp_path / "config.json"
    report = tmp_path / "report.md"
    _write_config(config)

    code = run_cli(["analyze", "-c", str(config), "-f", "md", "-o", str(report)])

    assert code == 0
    assert report.exists()
    content = report.read_text(encoding="utf-8")
    assert "SKO CERTIFIKAT SIGURNOSTI PLENUMA" in content


def test_cli_missing_config_returns_error():
    code = run_cli(["analyze", "-c", "missing-config.json", "-f", "json"])
    assert code == 1


def test_cli_version():
    """Verifikuje da CLI vraca verziju."""
    with pytest.raises(SystemExit) as exc_info:
        run_cli(["--version"])
    assert exc_info.value.code == 0


def test_cli_analyze_json_export(tmp_path):
    """Verifikuje pokretanje analyze komande sa JSON izvozom."""
    config_file = tmp_path / "config.json"
    output_file = tmp_path / "report.json"

    cfg_data = {
        "project_name": "CLI Test Project",
        "engineer_name": "Tester",
        "plenum_id": "PLENUM-CLI-01",
        "coverage_factor": 2.0,
        "inputs": {
            "velocity": {"value": 10.0, "uncertainty": 0.2, "unit_symbol": "m/s"}
        },
        "calculated_value": {"value": 100.0, "uncertainty": 2.0, "unit_symbol": "Pa"},
        "limit_value": {"value": 150.0, "uncertainty": 0.0, "unit_symbol": "Pa"},
    }

    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(cfg_data, f)

    exit_code = run_cli(
        [
            "analyze",
            "-c",
            str(config_file),
            "-o",
            str(output_file),
            "-f",
            "json",
        ]
    )

    assert exit_code == 0
    assert output_file.exists()

    with open(output_file, "r", encoding="utf-8") as f:
        result = json.load(f)

    assert result["metadata"]["project_name"] == "CLI Test Project"
    assert result["evaluation"]["status"] == "SAFE"
