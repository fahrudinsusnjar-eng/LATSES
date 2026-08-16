"""Translate independently verified site facts into structural load inputs.

This module never mutates or deletes environmental history. It only reads the
latest usable verified fact for each requested action and exposes a snapshot
for structural calculations.
"""
from __future__ import annotations

from dataclasses import dataclass

from lat_ces.building.environment import SiteEnvironment, SiteVerificationGate
from lat_ces.structural.load_ledger import LoadLedger


@dataclass(frozen=True)
class EnvironmentalLoadSnapshot:
    snow_ground_characteristic: float
    wind_basic_velocity: float
    wind_basic_pressure: float
    extreme_precipitation: float
    design_air_temperature: float


def build_environmental_load_snapshot(site: SiteEnvironment) -> EnvironmentalLoadSnapshot:
    """Return only independently verified climatic inputs.

    The verification gate is mandatory. Historical facts remain untouched in
    ``site.facts``; this function selects the latest verified fact per key.
    """
    gate = SiteVerificationGate()
    if not gate.ready_for_climatic_structural_analysis(site):
        raise ValueError("Site environment is not ready for structural climatic actions")
    return EnvironmentalLoadSnapshot(
        snow_ground_characteristic=site.require_verified("snow_ground_characteristic").value,
        wind_basic_velocity=site.require_verified("wind_basic_velocity").value,
        wind_basic_pressure=site.require_verified("wind_basic_pressure").value,
        extreme_precipitation=site.require_verified("extreme_precipitation").value,
        design_air_temperature=site.require_verified("design_air_temperature").value,
    )


def apply_environmental_actions(site: SiteEnvironment, ledger: LoadLedger) -> EnvironmentalLoadSnapshot:
    """Validate the site gate and return the immutable environmental snapshot.

    LoadLedger integration is intentionally a no-delete/read-only boundary;
    detailed EN 1991 load-combination rules remain in the structural layer.
    """
    return build_environmental_load_snapshot(site)
