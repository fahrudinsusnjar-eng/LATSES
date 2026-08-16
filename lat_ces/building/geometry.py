"""Small, dependency-free geometry primitives used by the building model.

Coordinates and dimensions are expressed in SI metres at this foundation layer.
Scientific quantities can be attached by downstream engines without changing the
building topology API.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Point3D:
    x: float
    y: float
    z: float

    def __post_init__(self) -> None:
        for name, value in (("x", self.x), ("y", self.y), ("z", self.z)):
            if not isinstance(value, (int, float)):
                raise TypeError(f"Point3D.{name} must be numeric")


@dataclass(frozen=True)
class Box3D:
    origin: Point3D
    length: float
    width: float
    height: float

    def __post_init__(self) -> None:
        for name, value in (
            ("length", self.length),
            ("width", self.width),
            ("height", self.height),
        ):
            if value <= 0:
                raise ValueError(f"Box3D.{name} must be > 0")

    @property
    def floor_area(self) -> float:
        return self.length * self.width

    @property
    def volume(self) -> float:
        return self.floor_area * self.height

    @property
    def max_point(self) -> Point3D:
        return Point3D(
            self.origin.x + self.length,
            self.origin.y + self.width,
            self.origin.z + self.height,
        )
