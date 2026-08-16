"""Canonical solver-neutral building fluid network primitives.

BUILDING-FLUID-001: connects shared BuildingModel element IDs to fluid
components without duplicating geometry. The module provides deterministic
reference calculations for incompressible steady flow, pressure loss and
fan/system balance; it does not replace the existing duct/plenum engines.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import pi


@dataclass(frozen=True)
class FluidNode:
    node_id: str
    building_element_id: str | None = None


@dataclass(frozen=True)
class FluidSegment:
    segment_id: str
    from_node: str
    to_node: str
    length_m: float
    diameter_m: float
    roughness_m: float = 0.00015
    minor_loss_k: float = 0.0

    def __post_init__(self) -> None:
        if not self.segment_id or not self.from_node or not self.to_node:
            raise ValueError("fluid segment identifiers must not be empty")
        if self.from_node == self.to_node:
            raise ValueError("fluid segment endpoints must differ")
        if self.length_m <= 0 or self.diameter_m <= 0:
            raise ValueError("fluid segment length and diameter must be positive")
        if self.roughness_m < 0 or self.minor_loss_k < 0:
            raise ValueError("roughness and minor loss coefficient must be non-negative")

    @property
    def area_m2(self) -> float:
        return pi * self.diameter_m**2 / 4.0

    @property
    def hydraulic_diameter_m(self) -> float:
        return self.diameter_m


@dataclass(frozen=True)
class FluidNetwork:
    nodes: tuple[FluidNode, ...]
    segments: tuple[FluidSegment, ...]

    def validate(self) -> None:
        ids = {node.node_id for node in self.nodes}
        if len(ids) != len(self.nodes):
            raise ValueError("duplicate fluid node IDs")
        for segment in self.segments:
            if segment.from_node not in ids or segment.to_node not in ids:
                raise ValueError(f"segment {segment.segment_id} references an unknown node")


def pressure_loss_pa(
    segment: FluidSegment,
    flow_m3_s: float,
    density_kg_m3: float,
    viscosity_pa_s: float,
) -> float:
    """Return Darcy-Weisbach + minor pressure loss for steady incompressible flow."""
    if flow_m3_s < 0:
        raise ValueError("flow must be non-negative")
    if density_kg_m3 <= 0 or viscosity_pa_s <= 0:
        raise ValueError("density and viscosity must be positive")
    velocity = flow_m3_s / segment.area_m2
    reynolds = density_kg_m3 * velocity * segment.hydraulic_diameter_m / viscosity_pa_s
    if reynolds == 0:
        friction_factor = 0.0
    elif reynolds < 2300:
        friction_factor = 64.0 / reynolds
    else:
        # Swamee-Jain explicit approximation for turbulent flow.
        relative_roughness = segment.roughness_m / segment.hydraulic_diameter_m
        friction_factor = 0.25 / (
            __import__("math").log10(relative_roughness / 3.7 + 5.74 / reynolds**0.9)
        ) ** 2
    dynamic_pressure = 0.5 * density_kg_m3 * velocity**2
    return (friction_factor * segment.length_m / segment.diameter_m + segment.minor_loss_k) * dynamic_pressure


def total_pressure_loss_pa(
    network: FluidNetwork,
    flows_m3_s: dict[str, float],
    density_kg_m3: float,
    viscosity_pa_s: float,
) -> float:
    network.validate()
    if set(flows_m3_s) != {s.segment_id for s in network.segments}:
        raise ValueError("a flow value is required for every segment")
    return sum(
        pressure_loss_pa(segment, flows_m3_s[segment.segment_id], density_kg_m3, viscosity_pa_s)
        for segment in network.segments
    )
