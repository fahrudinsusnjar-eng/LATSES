from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Mapping

from .reason_codes import ApplicabilityReason
from .registry import ModelRegistry


class ApplicabilityStatus(str, Enum):
    """Stable outcome statuses of the applicability gate."""

    APPLICABLE = "APPLICABLE"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    INVALID_INPUT = "INVALID_INPUT"
    MODEL_UNAVAILABLE = "MODEL_UNAVAILABLE"
    MODEL_SUPERSEDED = "MODEL_SUPERSEDED"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"


@dataclass(frozen=True)
class ApplicabilityRequest:
    """Input contract for an applicability evaluation."""

    model_id: str
    context: Mapping[str, object] | None = None
    inputs: Mapping[str, object] | None = None
    evidence: Mapping[str, object] | None = None
    model_version: str | None = None


@dataclass(frozen=True)
class ApplicabilityResult:
    """Deterministic result of an applicability evaluation."""

    status: ApplicabilityStatus
    applicable: bool
    model_id: str
    model_version: str | None
    reason_code: ApplicabilityReason
    rationale: str
    violations: tuple[str, ...] = ()
    validated_inputs: tuple[str, ...] = ()

    @property
    def is_applicable(self) -> bool:
        """Backward-compatible convenience property."""

        return self.applicable


class ApplicabilityEvaluator:
    """Evaluate whether a registered scientific model may be applied.

    This layer does not execute scientific equations.
    It only evaluates applicability and reports the reason.
    """

    def __init__(self, registry: ModelRegistry) -> None:
        self.registry = registry

    def evaluate(
        self,
        request: ApplicabilityRequest,
    ) -> ApplicabilityResult:
        """Evaluate model applicability without executing the model."""

        if not request.model_id.strip():
            return self._result(
                request,
                ApplicabilityStatus.MODEL_UNAVAILABLE,
                ApplicabilityReason.MODEL_NOT_REGISTERED,
                "No model identifier was supplied.",
            )

        if not self.registry.has(request.model_id):
            return self._result(
                request,
                ApplicabilityStatus.MODEL_UNAVAILABLE,
                ApplicabilityReason.MODEL_NOT_REGISTERED,
                f"Model '{request.model_id}' is not registered.",
            )

        entry = self.registry.get(request.model_id)

        if request.model_version is not None:
            if request.model_version != entry.version:
                return self._result(
                    request,
                    ApplicabilityStatus.MODEL_UNAVAILABLE,
                    ApplicabilityReason.MODEL_VERSION_UNAVAILABLE,
                    (
                        f"Requested model version '{request.model_version}' "
                        f"is unavailable; registered version is "
                        f"'{entry.version}'."
                    ),
                )

        if entry.status.value == "DEPRECATED":
            return self._result(
                request,
                ApplicabilityStatus.MODEL_SUPERSEDED,
                ApplicabilityReason.MODEL_SUPERSEDED,
                f"Model '{request.model_id}' is deprecated.",
            )

        if request.context is None:
            return self._result(
                request,
                ApplicabilityStatus.INSUFFICIENT_EVIDENCE,
                ApplicabilityReason.CONTEXT_MISSING,
                "No context was supplied for applicability evaluation.",
            )

        if not request.context:
            return self._result(
                request,
                ApplicabilityStatus.INSUFFICIENT_EVIDENCE,
                ApplicabilityReason.CONTEXT_INCOMPLETE,
                "The supplied context is incomplete.",
            )

        required_inputs = {
            item.name
            for item in entry.metadata.inputs
            if item.required
        }

        supplied_inputs = set((request.inputs or {}).keys())
        missing = required_inputs - supplied_inputs

        if missing:
            return self._result(
                request,
                ApplicabilityStatus.INVALID_INPUT,
                ApplicabilityReason.REQUIRED_INPUT_MISSING,
                "Required model inputs are missing.",
                violations=tuple(sorted(missing)),
            )

        return self._result(
            request,
            ApplicabilityStatus.APPLICABLE,
            ApplicabilityReason.APPLICABLE_INPUTS_VALID,
            "Model applicability requirements are satisfied.",
            validated_inputs=tuple(sorted(required_inputs)),
        )

    @staticmethod
    def _result(
        request: ApplicabilityRequest,
        status: ApplicabilityStatus,
        reason_code: ApplicabilityReason,
        rationale: str,
        *,
        violations: tuple[str, ...] = (),
        validated_inputs: tuple[str, ...] = (),
    ) -> ApplicabilityResult:
        return ApplicabilityResult(
            status=status,
            applicable=status is ApplicabilityStatus.APPLICABLE,
            model_id=request.model_id,
            model_version=request.model_version,
            reason_code=reason_code,
            rationale=rationale,
            violations=violations,
            validated_inputs=validated_inputs,
        )
