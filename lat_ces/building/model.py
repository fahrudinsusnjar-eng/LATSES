"""Canonical Building Model Foundation.

The model is deliberately topology-first: building, levels, rooms and generic
physical elements are represented before structural, fluid, thermal, acoustic
or electrical solvers are attached. All scalar geometric/material inputs are
SI values at this foundation boundary.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4

from .geometry import Box3D, Point3D


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid4()}"


def _positive(name: str, value: float) -> float:
    if not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be numeric")
    if value <= 0:
        raise ValueError(f"{name} must be > 0")
    return float(value)


@dataclass(frozen=True)
class Material:
    """Minimal material record shared by future physics engines.

    Optional properties are SI values: kg/m³, Pa, W/(m·K), and dimensionless
    Poisson ratio. No solver-specific behaviour belongs here.
    """

    name: str
    density: float | None = None
    youngs_modulus: float | None = None
    poisson_ratio: float | None = None
    thermal_conductivity: float | None = None
    material_id: str = field(default_factory=lambda: _id("MAT"))

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Material.name must not be empty")
        if self.density is not None and self.density <= 0:
            raise ValueError("Material.density must be > 0")
        if self.youngs_modulus is not None and self.youngs_modulus <= 0:
            raise ValueError("Material.youngs_modulus must be > 0")
        if self.thermal_conductivity is not None and self.thermal_conductivity <= 0:
            raise ValueError("Material.thermal_conductivity must be > 0")
        if self.poisson_ratio is not None and not (-1.0 < self.poisson_ratio < 0.5):
            raise ValueError("Material.poisson_ratio must be between -1 and 0.5")


@dataclass
class BuildingElement:
    """Generic physical element that can later be specialized by solver domains."""

    name: str
    geometry: Box3D
    element_type: str = "generic"
    material: Material | None = None
    element_id: str = field(default_factory=lambda: _id("ELM"))

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("BuildingElement.name must not be empty")
        if not self.element_type.strip():
            raise ValueError("BuildingElement.element_type must not be empty")


@dataclass
class Room:
    name: str
    footprint: Box3D
    room_id: str = field(default_factory=lambda: _id("ROOM"))
    elements: dict[str, BuildingElement] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Room.name must not be empty")

    @property
    def floor_area(self) -> float:
        return self.footprint.floor_area

    @property
    def volume(self) -> float:
        return self.footprint.volume

    def add_element(self, element: BuildingElement) -> BuildingElement:
        if element.element_id in self.elements:
            raise ValueError(f"Duplicate element id: {element.element_id}")
        self.elements[element.element_id] = element
        return element


@dataclass
class Level:
    name: str
    elevation: float
    height: float
    level_id: str = field(default_factory=lambda: _id("LVL"))
    rooms: dict[str, Room] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.height = _positive("Level.height", self.height)
        if not self.name.strip():
            raise ValueError("Level.name must not be empty")

    @property
    def top_elevation(self) -> float:
        return self.elevation + self.height

    @property
    def floor_area(self) -> float:
        return sum(room.floor_area for room in self.rooms.values())

    @property
    def volume(self) -> float:
        return sum(room.volume for room in self.rooms.values())

    def add_room(self, room: Room) -> Room:
        if room.room_id in self.rooms:
            raise ValueError(f"Duplicate room id: {room.room_id}")
        self.rooms[room.room_id] = room
        return room


@dataclass
class BuildingModel:
    """Topological source of truth for a building before domain solvers."""

    name: str
    model_id: str = field(default_factory=lambda: _id("BLDG"))
    levels: dict[str, Level] = field(default_factory=dict)
    materials: dict[str, Material] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("BuildingModel.name must not be empty")

    def add_level(self, level: Level) -> Level:
        if level.level_id in self.levels:
            raise ValueError(f"Duplicate level id: {level.level_id}")
        self.levels[level.level_id] = level
        return level

    def add_material(self, material: Material) -> Material:
        if material.material_id in self.materials:
            raise ValueError(f"Duplicate material id: {material.material_id}")
        self.materials[material.material_id] = material
        return material

    @property
    def floor_area(self) -> float:
        return sum(level.floor_area for level in self.levels.values())

    @property
    def volume(self) -> float:
        return sum(level.volume for level in self.levels.values())

    @property
    def room_count(self) -> int:
        return sum(len(level.rooms) for level in self.levels.values())

    @property
    def element_count(self) -> int:
        return sum(
            len(room.elements)
            for level in self.levels.values()
            for room in level.rooms.values()
        )

    def all_rooms(self) -> tuple[Room, ...]:
        return tuple(room for level in self.levels.values() for room in level.rooms.values())

    def all_elements(self) -> tuple[BuildingElement, ...]:
        return tuple(
            element
            for room in self.all_rooms()
            for element in room.elements.values()
        )

    def validate(self) -> list[str]:
        """Return structural/topological validation findings without mutating the model."""
        findings: list[str] = []
        elevations = sorted((level.elevation, level) for level in self.levels.values())
        for (_, lower), (upper_elevation, _) in zip(elevations, elevations[1:]):
            if lower.top_elevation > upper_elevation:
                findings.append(
                    f"Level overlap: {lower.level_id} reaches {lower.top_elevation} m "
                    f"above next elevation {upper_elevation} m"
                )
        return findings
