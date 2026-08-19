"""Solver-neutral preliminary vertical load-path analysis.

This module deliberately stops before code-based member design or safety-factor
selection. It aggregates declared permanent/imposed/roof/snow actions and
transfers them through storeys to foundation supports.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class FloorAction:
    """Area load assigned to a level, in kN/m²."""

    level_name: str
    area_m2: float
    permanent_kn_m2: float = 0.0
    imposed_kn_m2: float = 0.0
    snow_kn_m2: float = 0.0

    def __post_init__(self) -> None:
        if not self.level_name.strip():
            raise ValueError("level_name must not be empty")
        if self.area_m2 <= 0:
            raise ValueError("area_m2 must be > 0")
        for name, value in (("permanent_kn_m2", self.permanent_kn_m2), ("imposed_kn_m2", self.imposed_kn_m2), ("snow_kn_m2", self.snow_kn_m2)):
            if value < 0:
                raise ValueError(f"{name} must be >= 0")

    @property
    def permanent_kn(self) -> float:
        return self.area_m2 * self.permanent_kn_m2

    @property
    def imposed_kn(self) -> float:
        return self.area_m2 * self.imposed_kn_m2

    @property
    def snow_kn(self) -> float:
        return self.area_m2 * self.snow_kn_m2


@dataclass(frozen=True)
class VerticalElement:
    """Declared vertical carrier for gravity load transfer."""

    element_id: str
    element_type: str
    level_name: str
    capacity_class: str | None = None


@dataclass(frozen=True)
class LoadPathStep:
    from_level: str
    to_level: str
    permanent_kn: float
    imposed_kn: float
    snow_kn: float
    total_kn: float


@dataclass(frozen=True)
class FoundationReaction:
    support_id: str
    permanent_kn: float
    imposed_kn: float
    snow_kn: float
    total_kn: float


@dataclass(frozen=True)
class PreliminaryAnalysisResult:
    status: str
    floor_actions: tuple[FloorAction, ...]
    load_path: tuple[LoadPathStep, ...]
    foundation_reactions: tuple[FoundationReaction, ...]
    findings: tuple[str, ...] = ()

    @property
    def total_gravity_kn(self) -> float:
        return sum(item.total_kn for item in self.foundation_reactions)


@dataclass
class PreliminaryStructuralAnalysis:
    """Deterministic accumulation of declared vertical actions."""

    floor_actions: list[FloorAction] = field(default_factory=list)
    vertical_elements: list[VerticalElement] = field(default_factory=list)
    foundation_support_ids: tuple[str, ...] = ("FOUNDATION",)

    def add_floor_action(self, action: FloorAction) -> FloorAction:
        self.floor_actions.append(action)
        return action

    def add_vertical_element(self, element: VerticalElement) -> VerticalElement:
        self.vertical_elements.append(element)
        return element

    def evaluate(self) -> PreliminaryAnalysisResult:
        findings: list[str] = []
        if not self.floor_actions:
            findings.append("No floor actions supplied")

        known_levels = {action.level_name for action in self.floor_actions}
        carriers_by_level: dict[str, list[VerticalElement]] = {}
        for element in self.vertical_elements:
            carriers_by_level.setdefault(element.level_name, []).append(element)

        for level_name in sorted(known_levels):
            if level_name not in carriers_by_level:
                findings.append(f"No declared vertical load carrier at level: {level_name}")

        running_permanent = 0.0
        running_imposed = 0.0
        running_snow = 0.0
        steps: list[LoadPathStep] = []
        ordered = list(self.floor_actions)
        for index, action in enumerate(ordered):
            running_permanent += action.permanent_kn
            running_imposed += action.imposed_kn
            running_snow += action.snow_kn
            to_level = ordered[index + 1].level_name if index + 1 < len(ordered) else "FOUNDATION"
            steps.append(
                LoadPathStep(
                    from_level=action.level_name,
                    to_level=to_level,
                    permanent_kn=running_permanent,
                    imposed_kn=running_imposed,
                    snow_kn=running_snow,
                    total_kn=running_permanent + running_imposed + running_snow,
                )
            )

        reactions = tuple(
            FoundationReaction(
                support_id=support_id,
                permanent_kn=running_permanent,
                imposed_kn=running_imposed,
                snow_kn=running_snow,
                total_kn=running_permanent + running_imposed + running_snow,
            )
            for support_id in self.foundation_support_ids
        )

        status = "READY_PRELIMINARY" if not findings else "INPUT_REQUIRED"
        return PreliminaryAnalysisResult(
            status=status,
            floor_actions=tuple(ordered),
            load_path=tuple(steps),
            foundation_reactions=reactions,
            findings=tuple(findings),
        )


__all__ = [
    "FoundationReaction",
    "FloorAction",
    "LoadPathStep",
    "PreliminaryAnalysisResult",
    "PreliminaryStructuralAnalysis",
    "VerticalElement",
]
