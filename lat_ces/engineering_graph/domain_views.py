"""Domain-specific read-only views over the canonical engineering lineage."""
from __future__ import annotations

from .readonly import ReadOnlyEngineeringInputs


def structural_inputs(view: ReadOnlyEngineeringInputs) -> ReadOnlyEngineeringInputs:
    return view


def fluid_inputs(view: ReadOnlyEngineeringInputs) -> ReadOnlyEngineeringInputs:
    return view


def thermal_inputs(view: ReadOnlyEngineeringInputs) -> ReadOnlyEngineeringInputs:
    return view
