import math
from lat_ces.core.dimensions import DENSITY, VELOCITY
from lat_ces.modules.quantity import PhysicalQuantity
from lat_ces.modules.pressure import PRESSURE
from lat_ces.modules.fittings import FittingLossEngine


def test_fitting_loss():
    engine = FittingLossEngine()

    zeta = 0.5
    rho = PhysicalQuantity(1.2, DENSITY, 0.01)
    v = PhysicalQuantity(4.0, VELOCITY, 0.1)

    dp = engine.calculate_fitting_loss(zeta, rho, v)

    assert math.isclose(dp.value, 4.8, abs_tol=1e-2)
    assert dp.dimension == PRESSURE
    assert dp.uncertainty > 0