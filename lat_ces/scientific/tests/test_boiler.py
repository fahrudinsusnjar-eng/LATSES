import pytest
from lat_ces.scientific.boiler import BoilerModel, BoilerError


def test_boiler_fuel_consumption():
    model = BoilerModel(efficiency=0.9)
    fuel = model.compute_fuel_consumption(heat_output_kW=100.0, heating_value_kWh_m3=10.0)
    assert fuel > 0.0
