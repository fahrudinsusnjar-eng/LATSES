"""Engineering integration for BuildingModel-owned MEP objects.

GUI code calls this service; engineering calculations stay here or in the
canonical scientific engines. Results are stored on BuildingModel.mep so the
GUI can display them without owning scientific state.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import pi
from typing import Any

from lat_ces.building_model.systems import HeatingZone, VentilationOpening, WaterBranch
from lat_ces.core.dimensions import DENSITY, DYNAMIC_VISCOSITY, LENGTH, VELOCITY
from lat_ces.scientific.duct_friction import DuctFrictionModel
from lat_ces.scientific.pressure_drop import PressureDropModel
from lat_ces.scientific.quantity import PhysicalQuantity


@dataclass(frozen=True)
class EngineeringResult:
    object_type: str
    object_id: str
    status: str
    values: dict[str, Any]
    message: str = ""


class EngineeringResultRegistry:
    """Mutable engineering-result store owned by one BuildingModel MEP registry."""

    def __init__(self) -> None:
        self._results: dict[tuple[str, str], EngineeringResult] = {}

    def put(self, result: EngineeringResult) -> EngineeringResult:
        self._results[(result.object_type, result.object_id)] = result
        return result

    def get(self, object_type: str, object_id: str) -> EngineeringResult | None:
        return self._results.get((object_type, object_id))

    def remove(self, object_type: str, object_id: str) -> EngineeringResult | None:
        return self._results.pop((object_type, object_id), None)

    @property
    def all(self) -> tuple[EngineeringResult, ...]:
        return tuple(self._results.values())


def ensure_engineering_results(registry: object) -> EngineeringResultRegistry:
    results = getattr(registry, "engineering_results", None)
    if results is None:
        results = EngineeringResultRegistry()
        setattr(registry, "engineering_results", results)
    if not isinstance(results, EngineeringResultRegistry):
        raise TypeError("MEP engineering_results must be an EngineeringResultRegistry")
    return results


class MEPEngineeringService:
    """Dispatch selected MEP objects to canonical scientific calculations."""

    WATER_CP_J_KG_K = 4180.0

    def __init__(self, *, water_density_kg_m3: float = 998.2, water_dynamic_viscosity_pa_s: float = 1.002e-3) -> None:
        if water_density_kg_m3 <= 0.0 or water_dynamic_viscosity_pa_s <= 0.0:
            raise ValueError("Water density and dynamic viscosity must be positive")
        self.water_density = water_density_kg_m3
        self.water_viscosity = water_dynamic_viscosity_pa_s

    def calculate_ventilation(self, opening: VentilationOpening) -> EngineeringResult:
        area = opening.area_m2
        flow = opening.design_flow_m3_s
        velocity = opening.design_velocity_m_s
        pressure = PressureDropModel(loss_coefficient=1.0, air_density=1.2).compute_pressure_drop(velocity)
        return EngineeringResult(
            object_type="ventilation",
            object_id=opening.id,
            status="CALCULATED",
            values={
                "area_m2": area,
                "design_flow_m3_s": flow,
                "design_flow_m3_h": opening.design_flow_m3_h,
                "design_velocity_m_s": velocity,
                "reference_local_pressure_drop_pa": pressure,
            },
            message="Ventilation opening evaluated with the canonical pressure-drop model.",
        )

    def calculate_water(self, branch: WaterBranch) -> EngineeringResult:
        area = pi * branch.diameter_m**2 / 4.0
        velocity = branch.design_flow_m3_s / area if area > 0.0 else 0.0
        density = PhysicalQuantity(self.water_density, dimension=DENSITY)
        velocity_q = PhysicalQuantity(velocity, dimension=VELOCITY)
        diameter_q = PhysicalQuantity(branch.diameter_m, dimension=LENGTH)
        viscosity_q = PhysicalQuantity(self.water_viscosity, dimension=DYNAMIC_VISCOSITY)
        if velocity == 0.0:
            return EngineeringResult(
                object_type="water",
                object_id=branch.id,
                status="INPUT_REQUIRED",
                values={"cross_section_m2": area, "velocity_m_s": 0.0},
                message="Design flow must be greater than zero for hydraulic evaluation.",
            )
        reynolds = DuctFrictionModel.calculate_reynolds_number(density, velocity_q, diameter_q, viscosity_q)
        friction_factor = DuctFrictionModel.estimate_friction_factor(reynolds)
        pressure_drop = DuctFrictionModel(friction_factor=friction_factor).compute_friction_loss(
            length_m=branch.length_m,
            diameter_m=branch.diameter_m,
            velocity_m_s=velocity,
            air_density=self.water_density,
        )
        return EngineeringResult(
            object_type="water",
            object_id=branch.id,
            status="CALCULATED",
            values={
                "cross_section_m2": area,
                "velocity_m_s": velocity,
                "reynolds": reynolds,
                "friction_factor": friction_factor,
                "pressure_drop_pa": pressure_drop,
                "water_density_kg_m3": self.water_density,
                "dynamic_viscosity_pa_s": self.water_viscosity,
            },
            message="Water branch evaluated with the canonical Reynolds/Darcy-Weisbach model.",
        )

    def calculate_heating(self, zone: HeatingZone) -> EngineeringResult:
        delta_t = zone.design_supply_temp_c - zone.design_return_temp_c
        mean_water_temp = (zone.design_supply_temp_c + zone.design_return_temp_c) / 2.0
        values: dict[str, Any] = {
            "design_delta_t_k": delta_t,
            "mean_water_temperature_c": mean_water_temp,
            "specific_heat_capacity_j_kg_k": self.WATER_CP_J_KG_K,
        }

        if zone.mass_flow_kg_s is None and zone.room_heat_load_w is None:
            return EngineeringResult(
                object_type="heating",
                object_id=zone.id,
                status="INPUT_REQUIRED",
                values={**values, "required_input": "mass_flow_kg_s or room_heat_load_w"},
                message="Heating calculation requires a real mass flow or room heat load.",
            )

        calculated_heat_load = None
        calculated_mass_flow = None
        if zone.mass_flow_kg_s is not None:
            calculated_mass_flow = zone.mass_flow_kg_s
            calculated_heat_load = zone.mass_flow_kg_s * self.WATER_CP_J_KG_K * delta_t
            values["mass_flow_kg_s"] = zone.mass_flow_kg_s
            values["calculated_heat_load_w"] = calculated_heat_load

        if zone.room_heat_load_w is not None:
            values["room_heat_load_w"] = zone.room_heat_load_w
            if delta_t <= 0.0:
                raise ValueError("Heating delta T must be positive")
            implied_mass_flow = zone.room_heat_load_w / (self.WATER_CP_J_KG_K * delta_t)
            values["implied_mass_flow_kg_s"] = implied_mass_flow
            calculated_mass_flow = calculated_mass_flow or implied_mass_flow
            calculated_heat_load = calculated_heat_load or zone.room_heat_load_w

            if zone.mass_flow_kg_s is not None:
                mismatch = calculated_heat_load - zone.room_heat_load_w
                values["heat_load_difference_w"] = mismatch
                tolerance = max(1.0, abs(zone.room_heat_load_w) * 0.01)
                if abs(mismatch) > tolerance:
                    return EngineeringResult(
                        object_type="heating",
                        object_id=zone.id,
                        status="INPUT_CONFLICT",
                        values=values,
                        message="Provided room heat load and mass flow are inconsistent beyond the 1% engineering tolerance.",
                    )

        values["mass_flow_kg_s"] = calculated_mass_flow
        values["heat_rate_w"] = calculated_heat_load
        values["heat_rate_kw"] = calculated_heat_load / 1000.0
        return EngineeringResult(
            object_type="heating",
            object_id=zone.id,
            status="CALCULATED",
            values=values,
            message="Heating zone evaluated from the provided design heat load and/or water mass flow.",
        )

    def calculate(self, object_type: str, obj: object) -> EngineeringResult:
        if object_type == "ventilation" and isinstance(obj, VentilationOpening):
            return self.calculate_ventilation(obj)
        if object_type == "water" and isinstance(obj, WaterBranch):
            return self.calculate_water(obj)
        if object_type == "heating" and isinstance(obj, HeatingZone):
            return self.calculate_heating(obj)
        raise TypeError(f"Unsupported MEP object for calculation: {object_type}")


__all__ = [
    "EngineeringResult",
    "EngineeringResultRegistry",
    "MEPEngineeringService",
    "ensure_engineering_results",
]
