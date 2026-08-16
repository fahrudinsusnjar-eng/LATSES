from __future__ import annotations

import argparse
import sys
from pathlib import Path

from lat_ces.application.service import analyze_config, export_report, load_config, parse_quantity_dict
from lat_ces.scientific.quantity import PhysicalQuantity

# Compatibility exports: existing callers may still import the parser or
# PhysicalQuantity from the historical scientific CLI module while the
# implementation lives in the shared application/scientific layers.
_parse_quantity_dict = parse_quantity_dict


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
    analyze_parser.add_argument("-c", "--config", required=True, help="Path to JSON configuration file")
    analyze_parser.add_argument("-o", "--output", help="Output report path (e.g. report.pdf)")
    analyze_parser.add_argument(
        "-f", "--format", choices=["pdf", "json", "md"], default="pdf", help="Export format (default: pdf)"
    )

    parsed = parser.parse_args(args)
    if not parsed.command:
        parser.print_help()
        return 0

    if parsed.command == "analyze":
        try:
            config = load_config(Path(parsed.config))
            safety_report, exporter = analyze_config(
                config,
                project_default="LAT-CES CLI Analysis",
                plenum_default="PLENUM-CLI-01",
                equation_default="Custom equation",
            )
            output_file = parsed.output or f"report.{parsed.format}"
            output = export_report(exporter, output_file, parsed.format)
            print("Analysis completed successfully.")
            print(f"  Status: [{safety_report.status.value}]")
            print(f"  Export: {output} ({parsed.format.upper()})")
            return 0
        except Exception as error:
            print(f"Error while processing: {error}", file=sys.stderr)
            return 1

    return 0


def main():
    sys.exit(run_cli())


if __name__ == "__main__":
    main()
