import math
from lat_ces.modules.psychrometrics import PsychrometricEngine


def test_psychrometrics():
    engine = PsychrometricEngine()

    p_sat = engine.saturation_vapor_pressure_pa(20.0)
    assert math.isclose(p_sat, 2338.0, abs_tol=50.0)

    rh_100 = engine.calculate_relative_humidity(p_sat, 20.0)
    assert math.isclose(rh_100, 100.0, abs_tol=1e-2)