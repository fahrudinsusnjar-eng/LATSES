from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from lat_ces.scientific.analysis.plenum import SafetyReport, SafetyStatus
from lat_ces.scientific.devices.device import MeasurementDevice
from lat_ces.scientific.quantities.quantity import PhysicalQuantity


class SKOReportExporter:
    """Export engineering and metrology reports to JSON and Markdown."""

    def __init__(
        self,
        project_name: str,
        engineer_name: str,
        plenum_id: str,
        safety_report: SafetyReport,
        inputs: Dict[str, PhysicalQuantity],
        device: Optional[MeasurementDevice] = None,
        equation_name: Optional[str] = None,
    ):
        self.project_name = project_name
        self.engineer_name = engineer_name
        self.plenum_id = plenum_id
        self.safety_report = safety_report
        self.inputs = inputs
        self.device = device
        self.equation_name = equation_name or "Fizikalna Jednacina"
        self.timestamp = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Generate a structured dictionary with metrology traceability fields."""
        inputs_dict: Dict[str, Dict[str, Any]] = {}
        for key, quantity in self.inputs.items():
            inputs_dict[key] = {
                "value": quantity.value,
                "uncertainty": quantity.uncertainty,
                "relative_uncertainty_pct": round(quantity.relative_uncertainty * 100, 4),
                "unit_symbol": quantity.unit.symbol,
                "dimension": str(quantity.unit.dimension),
            }

        device_dict = None
        if self.device is not None:
            device_dict = {
                "name": self.device.name,
                "device_type": self.device.device_type,
                "unit": self.device.unit.symbol,
                "min_range": self.device.min_range,
                "max_range": self.device.max_range,
                "calibration_offset": self.device.calibration_offset,
                "uuid": self.device.uuid,
            }

        report = self.safety_report
        calculated = report.calculated_value
        limit = report.limit_value

        return {
            "metadata": {
                "project_name": self.project_name,
                "engineer_name": self.engineer_name,
                "plenum_id": self.plenum_id,
                "timestamp_utc": self.timestamp,
                "standard": "ISO GUM / LAT-CES Constitutional Science",
            },
            "device": device_dict,
            "inputs": inputs_dict,
            "equation": self.equation_name,
            "evaluation": {
                "status": report.status.value,
                "calculated_value": {
                    "value": calculated.value,
                    "uncertainty": calculated.uncertainty,
                    "unit_symbol": calculated.unit.symbol,
                },
                "limit_value": {
                    "value": limit.value,
                    "unit_symbol": limit.unit.symbol,
                },
                "coverage_factor_k": report.coverage_factor,
                "expanded_uncertainty": report.expanded_uncertainty,
                "margin_to_limit": report.margin_to_limit,
                "message": report.message,
            },
        }

    def to_json(self, indent: int = 2) -> str:
        """Generate a machine-readable JSON report."""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    def to_markdown(self) -> str:
        """Generate a markdown safety certificate report."""
        report = self.safety_report
        calculated = report.calculated_value
        limit = report.limit_value

        status_badge = {
            SafetyStatus.SAFE: "SAFE (SIGURNO)",
            SafetyStatus.METROLOGICAL_RISK: "METROLOGICAL RISK (UPOZORENJE)",
            SafetyStatus.CRITICAL_EXCEEDED: "CRITICAL EXCEEDED (KRITICNO)",
        }.get(report.status, report.status.value)

        markdown = []
        markdown.append("# 📜 SKO CERTIFIKAT SIGURNOSTI PLENUMA")
        markdown.append(
            f"**Projekat:** {self.project_name} | **Plenum ID:** `{self.plenum_id}`"
        )
        markdown.append(
            f"**Inzenjer:** {self.engineer_name} | **Datum:** {self.timestamp[:10]} (UTC)"
        )
        markdown.append("\n---")
        markdown.append("\n## 1. STATUS EVALUACIJE")
        markdown.append(f"\n### Status: {status_badge}")
        markdown.append(f"\n> **Rezime izvjestaja:** {report.message}")

        markdown.append("\n---")
        markdown.append("\n## 2. METROLOSKI I FIZIKALNI REZULTATI")
        markdown.append(
            "\n| Parametar | Nominalna Vrijednost | Mjerna Neodredjenost (u) | Jedinica | Relativna Neodredjenost |"
        )
        markdown.append("|---|---|---|---|---|")

        for name, quantity in self.inputs.items():
            markdown.append(
                f"| **Ulaz ({name})** | `{quantity.value:.4f}` | "
                f"`+/-{quantity.uncertainty:.4f}` | `{quantity.unit.symbol}` | "
                f"`{quantity.relative_uncertainty*100:.2f}%` |"
            )

        markdown.append(
            f"| **Izracunat Pritisak** | `{calculated.value:.4f}` | "
            f"`+/-{calculated.uncertainty:.4f}` | `{calculated.unit.symbol}` | "
            f"`{calculated.relative_uncertainty*100:.2f}%` |"
        )
        markdown.append(
            f"| **Dozvoljeni Limit** | `{limit.value:.4f}` | `-` | `{limit.unit.symbol}` | `-` |"
        )

        markdown.append("\n---")
        markdown.append("\n## 3. SIGURNOSNI RASPON I MARGINE (ISO GUM)")
        markdown.append(
            f"* **Prosirena neodredjenost (k={report.coverage_factor:.1f}, 95%):** "
            f"`+/-{report.expanded_uncertainty:.4f} {calculated.unit.symbol}`"
        )
        markdown.append(
            f"* **Gornja granica opsega (Worst-Case):** "
            f"`{calculated.value + report.expanded_uncertainty:.4f} {calculated.unit.symbol}`"
        )
        markdown.append(
            f"* **Nominalna margina do limita:** `{report.margin_to_limit:.4f} {calculated.unit.symbol}`"
        )

        if self.device is not None:
            markdown.append("\n---")
            markdown.append("\n## 4. SPECIFIKACIJA MJERNOG INSTRUMENTA")
            markdown.append(f"* **Naziv:** {self.device.name}")
            markdown.append(f"* **Tip uredjaja:** {self.device.device_type}")
            markdown.append(
                f"* **Radni opseg:** [{self.device.min_range} - {self.device.max_range}] "
                f"{self.device.unit.symbol}"
            )
            markdown.append(f"* **UUID Sljedivost:** `{self.device.uuid}`")

        markdown.append("\n---")
        markdown.append(
            "\n*Generisano automatski putem LAT-CES Scientific Core v1.0 (ISO GUM Compliant)*"
        )

        return "\n".join(markdown)


__all__ = ["SKOReportExporter"]