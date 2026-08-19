"""Integrated engineering analysis for the small reference building.

This is intentionally a thin orchestration layer: the BuildingModel remains the
single geometry source and the existing first-order engineering models consume
values derived from it. Detailed solvers can replace individual calculations
without changing the model contract.
"""
from dataclasses import dataclass
from typing import List

from .airflow import AirflowResult, calculate_airflow
from .core import BuildingModel
from .heating import HeatingResult, calculate_heat_load
from .validation import ValidationResult, validate_model
from .water import WaterResult, calculate_water_flow


@dataclass(frozen=True)
class BuildingEngineeringReport:
    validation: List[ValidationResult]
    airflow: AirflowResult
    water: WaterResult
    heating: HeatingResult


def analyze_building(
    model: BuildingModel,
    *,
    airflow_ach: float = 0.85,
    airflow_velocity_m_s: float = 0.05,
    water_flow_m3_s: float = 0.0002,
    water_diameter_m: float = 0.02,
    outdoor_temp_c: float = -5.0,
    indoor_temp_c: float = 20.0,
    u_value_w_m2k: float = 0.30,
    emitter_type: str = "underfloor",
) -> BuildingEngineeringReport:
    """Run the first integrated engineering pass from one BuildingModel.

    Airflow is derived from total modeled room volume and the requested ACH.
    The required low-velocity equivalent opening area is then calculated so the
    result explicitly exposes the physical consequence of a 0.05 m/s target.
    Heating uses the same room volume and airflow result. Water is a first-order
    branch calculation until the full pipe-network model is connected.
    """
    if airflow_ach < 0:
        raise ValueError("airflow_ach cannot be negative")

    validation = validate_model(model)
    room_area = sum(room.floor_area_m2 for level in model.levels.values() for room in level.rooms.values())
    room_volume = model.total_volume_m3()
    if room_volume <= 0:
        raise ValueError("building must contain rooms with positive volume")

    required_flow_m3_s = room_volume * airflow_ach / 3600.0
    equivalent_opening_area_m2 = required_flow_m3_s / airflow_velocity_m_s if airflow_velocity_m_s > 0 else 0.0
    airflow = calculate_airflow(
        equivalent_opening_area_m2,
        airflow_velocity_m_s,
        room_volume,
        target_velocity_m_s=0.05,
    )

    heating = calculate_heat_load(
        room_area,
        room_volume,
        indoor_temp_c - outdoor_temp_c,
        u_value_w_m2k,
        airflow.air_changes_per_hour,
        emitter_type=emitter_type,
    )
    water = calculate_water_flow(water_flow_m3_s, water_diameter_m)

    return BuildingEngineeringReport(
        validation=validation,
        airflow=airflow,
        water=water,
        heating=heating,
    )
