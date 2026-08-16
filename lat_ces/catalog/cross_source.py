"""Cross-source evidence comparison for technical product facts.

The manufacturer remains the primary declaration source. Other sources are
comparison evidence only; this module never selects an engineering value.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class CrossSourceStatus(str, Enum):
    CONSISTENT = "consistent"
    DISCREPANT = "discrepant"
    INSUFFICIENT = "insufficient"


@dataclass(frozen=True)
class SourceObservation:
    source_id: str
    source_type: str
    value: Any
    unit: str
    observed_at: str
    source_url: str
    primary: bool = False


@dataclass(frozen=True)
class CrossSourceCheck:
    product_id: str
    property_name: str
    primary_source_id: str
    observations: tuple[SourceObservation, ...]
    status: CrossSourceStatus
    compared_at: str


def compare_observations(
    product_id: str,
    property_name: str,
    observations: tuple[SourceObservation, ...],
    *,
    compared_at: str,
) -> CrossSourceCheck:
    primary = tuple(item for item in observations if item.primary)
    if len(primary) != 1:
        raise ValueError("exactly one primary manufacturer observation is required")
    if not observations:
        raise ValueError("at least one observation is required")

    primary_value = primary[0].value
    comparable = tuple(item for item in observations if item.unit == primary[0].unit)
    if len(comparable) < 2:
        status = CrossSourceStatus.INSUFFICIENT
    else:
        status = (
            CrossSourceStatus.CONSISTENT
            if all(item.value == primary_value for item in comparable)
            else CrossSourceStatus.DISCREPANT
        )

    return CrossSourceCheck(
        product_id=product_id,
        property_name=property_name,
        primary_source_id=primary[0].source_id,
        observations=observations,
        status=status,
        compared_at=compared_at,
    )
