"""Preliminary reinforced-concrete reinforcement model.

This module stores section, material, cover, bar layout and design actions for
concrete members. It intentionally stops at preliminary reinforcement sizing;
code-specific ULS/SLS verification, interaction diagrams, detailing rules and
national parameters must be supplied by the selected design code profile.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from math import pi


class RCElementType(str, Enum):
    BEAM = "beam"
    COLUMN = "column"
    SLAB = "slab"
    WALL = "wall"
    RING_BEAM = "ring_beam"
    FOUNDATION = "foundation"
    OTHER = "other"


@dataclass(frozen=True)
class ConcreteMaterial:
    grade: str
    fck_mpa: float

    def __post_init__(self) -> None:
        if not self.grade.strip() or self.fck_mpa <= 0:
            raise ValueError("concrete grade and fck_mpa are required")


@dataclass(frozen=True)
class ReinforcementSteel:
    grade: str
    fyk_mpa: float

    def __post_init__(self) -> None:
        if not self.grade.strip() or self.fyk_mpa <= 0:
            raise ValueError("steel grade and fyk_mpa are required")


@dataclass(frozen=True)
class RCSection:
    width_m: float
    depth_m: float
    cover_m: float
    length_m: float | None = None

    def __post_init__(self) -> None:
        for name, value in (("width_m", self.width_m), ("depth_m", self.depth_m), ("cover_m", self.cover_m)):
            if value <= 0:
                raise ValueError(f"{name} must be > 0")
        if self.length_m is not None and self.length_m <= 0:
            raise ValueError("length_m must be > 0")
        if 2 * self.cover_m >= min(self.width_m, self.depth_m):
            raise ValueError("cover is too large for the section")


@dataclass(frozen=True)
class Rebar:
    diameter_mm: float
    count: int
    face: str = "longitudinal"
    position: str = "main"

    @property
    def area_mm2(self) -> float:
        return self.count * pi * self.diameter_mm**2 / 4.0

    def __post_init__(self) -> None:
        if self.diameter_mm <= 0 or self.count <= 0:
            raise ValueError("rebar diameter and count must be > 0")


@dataclass(frozen=True)
class StirrupLayout:
    diameter_mm: float
    spacing_mm: float
    legs: int = 2
    zone: str = "standard"

    def __post_init__(self) -> None:
        if self.diameter_mm <= 0 or self.spacing_mm <= 0 or self.legs < 2:
            raise ValueError("invalid stirrup layout")


@dataclass(frozen=True)
class RCDesignActions:
    med_knm: float | None = None
    ved_kn: float | None = None
    ned_kn: float | None = None
    ped_kn: float | None = None


@dataclass
class ReinforcedConcreteElement:
    element_id: str
    element_type: RCElementType
    section: RCSection
    concrete: ConcreteMaterial
    steel: ReinforcementSteel
    actions: RCDesignActions = field(default_factory=RCDesignActions)
    longitudinal_bars: list[Rebar] = field(default_factory=list)
    stirrups: list[StirrupLayout] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    @property
    def provided_longitudinal_area_mm2(self) -> float:
        return sum(bar.area_mm2 for bar in self.longitudinal_bars)


@dataclass(frozen=True)
class PreliminaryRCDesignResult:
    status: str
    required_as_mm2: float | None
    provided_as_mm2: float
    utilisation: float | None
    findings: tuple[str, ...] = ()


def preliminary_flexural_steel_area(
    *,
    med_knm: float | None,
    section: RCSection,
    steel: ReinforcementSteel,
    z_factor: float = 0.9,
    min_as_mm2: float = 0.0,
) -> float | None:
    """Estimate As from MEd using As ~= MEd/(fyd*z).

    This is a screening equation, not a complete EN 1992 design check.
    A code profile must supply alpha-correction, fcd/fyd definitions, minimum
    reinforcement, compression reinforcement, shear and detailing checks.
    """
    if med_knm is None:
        return None
    if z_factor <= 0 or z_factor >= 1:
        raise ValueError("z_factor must be between 0 and 1")
    fyd_n_mm2 = steel.fyk_mpa / 1.15
    d_mm = (section.depth_m - section.cover_m) * 1000.0
    z_mm = z_factor * d_mm
    if z_mm <= 0:
        raise ValueError("effective depth must be > 0")
    as_mm2 = abs(med_knm) * 1_000_000.0 / (fyd_n_mm2 * z_mm)
    return max(as_mm2, min_as_mm2)


def evaluate_preliminary_rc_design(element: ReinforcedConcreteElement) -> PreliminaryRCDesignResult:
    required = preliminary_flexural_steel_area(
        med_knm=element.actions.med_knm,
        section=element.section,
        steel=element.steel,
    )
    provided = element.provided_longitudinal_area_mm2
    findings: list[str] = []

    if required is None:
        findings.append("MEd is required for preliminary flexural reinforcement sizing")
        return PreliminaryRCDesignResult("INPUT_REQUIRED", None, provided, None, tuple(findings))

    utilisation = required / provided if provided > 0 else None
    if provided <= 0:
        findings.append("No longitudinal reinforcement layout supplied")
        return PreliminaryRCDesignResult("INPUT_REQUIRED", required, provided, utilisation, tuple(findings))

    status = "PRELIMINARY_OK" if provided >= required else "REINFORCEMENT_REQUIRED"
    if element.element_type in {RCElementType.COLUMN, RCElementType.WALL} and element.actions.ned_kn is None:
        findings.append("NEd is required for axial/interaction verification")

    if not element.stirrups and element.element_type in {
        RCElementType.BEAM,
        RCElementType.COLUMN,
        RCElementType.RING_BEAM,
    }:
        findings.append("Transverse reinforcement layout is required for shear/confinement verification")

    return PreliminaryRCDesignResult(status, required, provided, utilisation, tuple(findings))


__all__ = [
    "ConcreteMaterial",
    "RCDesignActions",
    "RCElementType",
    "RCSection",
    "Rebar",
    "ReinforcedConcreteElement",
    "ReinforcementSteel",
    "StirrupLayout",
    "PreliminaryRCDesignResult",
    "evaluate_preliminary_rc_design",
    "preliminary_flexural_steel_area",
]
