"""Regression tests for the canonical pressure/duct/fan integration."""

from lat_ces.modules.fluid_network import FluidNetwork as LegacyFluidNetwork
from lat_ces.scientific.duct_friction import DuctFrictionModel
from lat_ces.scientific.fluid_network import FluidNetwork, FluidSegment
from lat_ces.scientific.pressure_drop import PressureDropModel


def test_fluid_network_composes_existing_models_without_changing_results():
    segment = FluidSegment(
        name="supply-main",
        length_m=10.0,
        diameter_m=0.2,
        velocity_m_s=4.0,
        friction_factor=0.02,
        loss_coefficient=1.2,
    )
    network = FluidNetwork([segment], air_density=1.2)

    expected_friction = DuctFrictionModel(friction_factor=0.02).compute_friction_loss(
        length_m=10.0,
        diameter_m=0.2,
        velocity_m_s=4.0,
        air_density=1.2,
    )
    expected_local = PressureDropModel(loss_coefficient=1.2, air_density=1.2).compute_pressure_drop(4.0)

    assert network.segment_pressure_drop(segment) == round(expected_friction + expected_local, 2)
    assert network.total_pressure_drop() == network.segment_pressure_drop(segment)


def test_fluid_network_operating_point_is_positive_and_deterministic():
    network = FluidNetwork(
        [
            FluidSegment(
                name="main",
                length_m=20.0,
                diameter_m=0.25,
                velocity_m_s=3.0,
                friction_factor=0.02,
                loss_coefficient=0.8,
            ),
            FluidSegment(
                name="branch",
                length_m=8.0,
                diameter_m=0.16,
                velocity_m_s=2.0,
                friction_factor=0.022,
                loss_coefficient=1.1,
            ),
        ],
        fan_max_pressure=500.0,
        fan_coefficient_a=200.0,
    )

    result = network.evaluate()

    assert result["segment_count"] == 2
    assert result["total_pressure_drop_pa"] > 0.0
    assert result["system_resistance"] > 0.0
    assert result["operating_flow"] > 0.0
    assert result == network.evaluate()


def test_legacy_facade_points_to_canonical_api():
    assert LegacyFluidNetwork is FluidNetwork
