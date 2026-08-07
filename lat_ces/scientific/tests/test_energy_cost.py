import pytest
from lat_ces.scientific.energy_cost import EnergyCostModel, EnergyCostError


def test_cost_calculation():
    model = EnergyCostModel(base_tariff_per_kwh=0.15)
    cost = model.compute_operational_cost(power_kw=2.5, duration_hours=2.0)
    assert cost > 0.0
