import pytest

from lat_ces.scientific.energy import EnergyEfficiencyModel, EnergyError


def test_sfp_calculation():
    model = EnergyEfficiencyModel()
    # Fan power = 1.5 kW, Airflow = 0.5 m^3/s -> SFP = 3.0 kW/(m^3/s)
    sfp = model.compute_specific_fan_power(fan_power_kw=1.5, airflow_m3s=0.5)
    assert sfp == pytest.approx(3.0, rel=1e-3)
