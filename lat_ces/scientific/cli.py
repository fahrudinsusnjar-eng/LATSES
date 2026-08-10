from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict

from lat_ces.scientific.analysis.plenum import PlenumAnalysisEngine
from lat_ces.scientific.dimensions.dimension import DIMENSIONLESS, LENGTH, MASS, TIME
from lat_ces.scientific.quantities.quantity import PhysicalQuantity
from lat_ces.scientific.reports.exporter import SKOReportExporter
from lat_ces.scientific.reports.pdf_generator import SKOPDFGenerator
from lat_ces.scientific.units.units import Unit


def _parse_quantity_dict(data: Dict[str, Any]) -> PhysicalQuantity:
    """Convert a JSON dictionary into a PhysicalQuantity instance."""
    symbol = data.get("unit_symbol", data.get("symbol", "Pa"))

    dim_map = {
        "m/s": LENGTH / TIME,
        "kg/m3": MASS / (LENGTH**3),
        "kg/m³": MASS / (LENGTH**3),
        "Pa": MASS / (LENGTH * (TIME**2)),
        "m2": LENGTH**2,
        "m²": LENGTH**2,
        "m3/s": (LENGTH**3) / TIME,
        "m³/s": (LENGTH**3) / TIME,
        "-": DIMENSIONLESS,
    }

    dimension = dim_map.get(symbol, DIMENSIONLESS)
    unit = Unit(symbol, symbol, dimension)
    value = float(data["value"])
    uncertainty = float(data.get("uncertainty", 0.0))
    return PhysicalQuantity(
        value,
        uncertainty,
        unit,
    )


def run_cli(args=None) -> int:
    """Run LAT-CES scientific analysis CLI."""
    parser = argparse.ArgumentParser(
        prog="lat-ces",
        description="LAT-CES Scientific Core - Plenum and Fluid Safety Analysis CLI",
    )
    parser.add_argument("--version", action="version", version="LAT-CES Scientific Core v1.0.0")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Run plenum analysis from JSON configuration",
    )
    analyze_parser.add_argument(
        "-c",
        "--config",
        required=True,
        help="Path to JSON configuration file",
    )
    analyze_parser.add_argument(
        "-o",
        "--output",
        help="Output report path (e.g. report.pdf)",
    )
    analyze_parser.add_argument(
        "-f",
        "--format",
        choices=["pdf", "json", "md"],
        default="pdf",
        help="Export format (default: pdf)",
    )

    parsed = parser.parse_args(args)

    if not parsed.command:
        parser.print_help()
        return 0

    if parsed.command == "analyze":
        config_path = Path(parsed.config)
        if not config_path.exists():
            print(f"Error: Config file '{config_path}' does not exist.", file=sys.stderr)
            return 1

        try:
            with open(config_path, "r", encoding="utf-8") as file:
                config = json.load(file)

            inputs = {name: _parse_quantity_dict(q) for name, q in config.get("inputs", {}).items()}
            calculated_q = _parse_quantity_dict(config["calculated_value"])
            limit_q = _parse_quantity_dict(config["limit_value"])

            coverage_factor = float(config.get("coverage_factor", 2.0))
            safety_report = PlenumAnalysisEngine.evaluate_limit(
                calculated=calculated_q,
                limit=limit_q,
                coverage_factor=coverage_factor,
            )

            exporter = SKOReportExporter(
                project_name=config.get("project_name", "LAT-CES CLI Analysis"),
                engineer_name=config.get("engineer_name", "Engineer"),
                plenum_id=config.get("plenum_id", "PLENUM-CLI-01"),
                safety_report=safety_report,
                inputs=inputs,
                equation_name=config.get("equation_name", "Custom equation"),
            )

            report_format = parsed.format
            output_file = parsed.output or f"report.{report_format}"

            if report_format == "json":
                with open(output_file, "w", encoding="utf-8") as file:
                    file.write(exporter.to_json())
            elif report_format == "md":
                with open(output_file, "w", encoding="utf-8") as file:
                    file.write(exporter.to_markdown())
            else:
                SKOPDFGenerator.generate_pdf(exporter, output_file)

            print("Analysis completed successfully.")
            print(f"  Status: [{safety_report.status.value}]")
            print(f"  Export: {output_file} ({report_format.upper()})")
            return 0
        except Exception as error:
            print(f"Error while processing: {error}", file=sys.stderr)
            return 1

    return 0


def main():
    sys.exit(run_cli())


if __name__ == "__main__":
    main()