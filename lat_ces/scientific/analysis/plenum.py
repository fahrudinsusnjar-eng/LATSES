from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from lat_ces.scientific.equations.engine import DimensionalityError
from lat_ces.scientific.quantities.quantity import PhysicalQuantity


class SafetyStatus(Enum):
    SAFE = "SAFE"
    METROLOGICAL_RISK = "METROLOGICAL_RISK"
    CRITICAL_EXCEEDED = "CRITICAL_EXCEEDED"


@dataclass
class SafetyReport:
    status: SafetyStatus
    calculated_value: PhysicalQuantity
    limit_value: PhysicalQuantity
    expanded_uncertainty: float
    coverage_factor: float
    margin_to_limit: float
    message: str


class PlenumAnalysisEngine:
    """Evaluate plenum and duct safety margins under measured uncertainty."""

    @staticmethod
    def evaluate_limit(
        calculated: PhysicalQuantity,
        limit: PhysicalQuantity,
        coverage_factor: float = 2.0,
    ) -> SafetyReport:
        """Compare a calculated quantity with a limit using expanded uncertainty."""
        if calculated.unit.dimension != limit.unit.dimension:
            raise DimensionalityError(
                "Nemoguće porediti fizikalne veličine različitih dimenzija: "
                f"{calculated.unit.dimension} vs {limit.unit.dimension}."
            )

        limit_converted_value = (
            limit.value * limit.unit.scale_factor
        ) / calculated.unit.scale_factor
        expanded_uncertainty = calculated.uncertainty * coverage_factor
        margin = limit_converted_value - calculated.value

        if calculated.value > limit_converted_value:
            status = SafetyStatus.CRITICAL_EXCEEDED
            message = (
                f"KRITIČNO: Nominalna vrijednost ({calculated.value:.2f} "
                f"{calculated.unit.symbol}) premašuje dozvoljeni limit od "
                f"{limit_converted_value:.2f} {calculated.unit.symbol}."
            )
        elif calculated.value + expanded_uncertainty > limit_converted_value:
            status = SafetyStatus.METROLOGICAL_RISK
            message = (
                f"UPOZORENJE (METROLOŠKI RIZIK): Nominalna vrijednost "
                f"({calculated.value:.2f} {calculated.unit.symbol}) je unutar "
                f"granica, ali proširena neodređenost (±{expanded_uncertainty:.2f}, "
                f"k={coverage_factor:.1f}) probija dozvoljeni limit od "
                f"{limit_converted_value:.2f} {calculated.unit.symbol}."
            )
        else:
            status = SafetyStatus.SAFE
            message = (
                f"SIGURNO: Vrijednost sa proširenom neodređenošću "
                f"({calculated.value + expanded_uncertainty:.2f} "
                f"{calculated.unit.symbol}) je pod potpunom kontrolom unutar "
                f"limita od {limit_converted_value:.2f} {calculated.unit.symbol}."
            )

        return SafetyReport(
            status=status,
            calculated_value=calculated,
            limit_value=limit,
            expanded_uncertainty=expanded_uncertainty,
            coverage_factor=coverage_factor,
            margin_to_limit=margin,
            message=message,
        )


__all__ = ["SafetyStatus", "SafetyReport", "PlenumAnalysisEngine"]