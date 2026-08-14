from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple

from lat_ces.scientific.dimensions.dimension import Dimension


@dataclass(frozen=True)
class ModelInput:
    """Describes one scientific-model input."""

    name: str
    description: str
    dimension: Dimension
    required: bool = True


@dataclass(frozen=True)
class ModelOutput:
    """Describes one scientific-model output."""

    name: str
    description: str
    dimension: Dimension


@dataclass(frozen=True)
class ScientificModelMetadata:
    """Declarative metadata for a scientific model.

    This class is intentionally independent from PhysicalEquation.
    Existing equation implementations remain unchanged and continue
    to perform the actual numerical calculation.
    """

    model_id: str
    name: str
    domain: str
    description: str
    equation: str

    inputs: Tuple[ModelInput, ...]
    outputs: Tuple[ModelOutput, ...]

    assumptions: Tuple[str, ...] = ()
    validity: Tuple[str, ...] = ()
    references: Tuple[str, ...] = ()

    equation_class: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.model_id:
            raise ValueError("model_id must not be empty.")
        if not self.name:
            raise ValueError("name must not be empty.")
        if not self.domain:
            raise ValueError("domain must not be empty.")
        if not self.equation:
            raise ValueError("equation must not be empty.")
        if not self.inputs:
            raise ValueError("A scientific model must define at least one input.")
        if not self.outputs:
            raise ValueError("A scientific model must define at least one output.")

    @property
    def input_names(self) -> Tuple[str, ...]:
        return tuple(item.name for item in self.inputs)

    @property
    def output_names(self) -> Tuple[str, ...]:
        return tuple(item.name for item in self.outputs)
