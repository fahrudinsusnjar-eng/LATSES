from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from lat_ces.scientific.dimensions.dimension import Dimension

from .metadata import ModelInput, ModelOutput, ScientificModelMetadata


@dataclass(frozen=True)
class ContractIssue:
    """One deterministic scientific-model contract violation."""

    code: str
    message: str


class ScientificModelContract:
    """Validate the structural contract of a scientific model.

    This layer validates metadata only. It does not execute equations
    and does not replace PhysicalEquation validation.
    """

    def __init__(self, metadata: ScientificModelMetadata) -> None:
        self.metadata = metadata

    def validate_inputs(self) -> tuple[ContractIssue, ...]:
        issues: list[ContractIssue] = []
        issues.extend(self._check_unique_names(self.metadata.inputs, code="DUPLICATE_INPUT", kind="input"))
        for item in self.metadata.inputs:
            if not item.name.strip():
                issues.append(ContractIssue("EMPTY_INPUT_NAME", "Input name must not be empty."))
            if not item.description.strip():
                issues.append(ContractIssue("EMPTY_INPUT_DESCRIPTION", f"Input '{item.name}' must have a description."))
        return tuple(issues)

    def validate_outputs(self) -> tuple[ContractIssue, ...]:
        issues: list[ContractIssue] = []
        issues.extend(self._check_unique_names(self.metadata.outputs, code="DUPLICATE_OUTPUT", kind="output"))
        for item in self.metadata.outputs:
            if not item.name.strip():
                issues.append(ContractIssue("EMPTY_OUTPUT_NAME", "Output name must not be empty."))
            if not item.description.strip():
                issues.append(ContractIssue("EMPTY_OUTPUT_DESCRIPTION", f"Output '{item.name}' must have a description."))
        return tuple(issues)

    def validate_dimensions(self) -> tuple[ContractIssue, ...]:
        issues: list[ContractIssue] = []
        for item in (*self.metadata.inputs, *self.metadata.outputs):
            if not isinstance(item.dimension, Dimension):
                issues.append(ContractIssue("INVALID_DIMENSION", f"'{item.name}' does not contain a valid Dimension."))
        return tuple(issues)

    def validate(self) -> tuple[ContractIssue, ...]:
        return (*self.validate_inputs(), *self.validate_outputs(), *self.validate_dimensions())

    @property
    def is_valid(self) -> bool:
        return not self.validate()

    @staticmethod
    def _check_unique_names(items: Iterable[ModelInput | ModelOutput], *, code: str, kind: str) -> tuple[ContractIssue, ...]:
        seen: set[str] = set()
        issues: list[ContractIssue] = []
        for item in items:
            if item.name in seen:
                issues.append(ContractIssue(code, f"Duplicate {kind} name: '{item.name}'."))
            seen.add(item.name)
        return tuple(issues)
