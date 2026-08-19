"""Solver-neutral preliminary vertical load-path analysis."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class FloorAction:
    level: str
    area_m2: float
    permanent_kn_m2: float = 0.0
    imposed_kn_m2: float = 0.0
    snow_kn_m2: float = 0.0

    def __post_init__(self) -> None:
        if not self.level.strip():
            raise ValueError("FloorAction.level must not be empty")
        if self.area_m2 <= 0:
            raise ValueError("FloorAction.area_m2 must be > 0")
        for name, value in (
            ("permanent_kn_m2", self.permanent_kn_m2),
            ("imposed_kn_m2", self.imposed_kn_m2),
            ("snow_kn_m2", self.snow_kn_m2),
        ):
            if value < 0:
                raise ValueError(f"{name} must be >= 0")


@dataclass(frozen=True)
class VerticalElement:
    element_id: str
    element_type: str
    level: str


@dataclass(frozen=True)
class LoadPathStep:
    level: str
    permanent_kn: float
    imposed_kn: float
    snow_kn: float

    @property
    def total_kn(self) -> float:
        return self.permanent_kn + self.imposed_kn + self.snow_kn


@dataclass(frozen=True)
class FoundationReaction:
    element_id: str
    total_kn: float


@dataclass(frozen=True)
class PreliminaryStructuralResult:
    status: str
    load_path: tuple[LoadPathStep, ...] = ()
    foundation_reactions: tuple[FoundationReaction, ...] = ()
    findings: tuple[str, ...] = ()
    total_gravity_kn: float = 0.0


@dataclass
class PreliminaryStructuralAnalysis:
    floor_actions: list[FloorAction] = field(default_factory=list)
    vertical_elements: list[VerticalElement] = field(default_factory=list)

    def add_floor_action(self, action: FloorAction) -> FloorAction:
        self.floor_actions.append(action)
        return action

    def add_vertical_element(self, element: VerticalElement) -> VerticalElement:
        self.vertical_elements.append(element)
        return element

    def evaluate(self) -> PreliminaryStructuralResult:
        findings: list[str] = []
        carriers_by_level: dict[str, list[VerticalElement]] = {}
        for element in self.vertical_elements:
            if element.element_type in {
                "load-bearing-wall",
                "column",
                "shear-wall",
                "foundation",
            }:
                carriers_by_level.setdefault(element.level, []).append(element)

        for action in self.floor_actions:
            if action.level not in carriers_by_level:
                findings.append(
                    f"No declared vertical load carrier at level: {action.level}"
                )

        if findings:
            return PreliminaryStructuralResult(
                status="INPUT_REQUIRED",
                findings=tuple(findings),
            )

        ordered = list(self.floor_actions)
        load_path: list[LoadPathStep] = []
        permanent_total = 0.0
        imposed_total = 0.0
        snow_total = 0.0
        for action in ordered:
            permanent_total += action.area_m2 * action.permanent_kn_m2
            imposed_total += action.area_m2 * action.imposed_kn_m2
            snow_total += action.area_m2 * action.snow_kn_m2
            load_path.append(
                LoadPathStep(
                    level=action.level,
                    permanent_kn=permanent_total,
                    imposed_kn=imposed_total,
                    snow_kn=snow_total,
                )
            )

        total = permanent_total + imposed_total + snow_total
        carriers = [
            element
            for element in self.vertical_elements
            if element.element_type
            in {"load-bearing-wall", "column", "shear-wall", "foundation"}
        ]
        share = total / len(carriers) if carriers else 0.0
        reactions = tuple(
            FoundationReaction(element.element_id, share) for element in carriers
        )
        return PreliminaryStructuralResult(
            status="READY_PRELIMINARY",
            load_path=tuple(load_path),
            foundation_reactions=reactions,
            findings=(),
            total_gravity_kn=total,
        )


__all__ = [
    "FloorAction",
    "FoundationReaction",
    "LoadPathStep",
    "PreliminaryStructuralAnalysis",
    "PreliminaryStructuralResult",
    "VerticalElement",
]
