import math
from lat_ces.core.dimensions import DENSITY, VELOCITY, LENGTH
from lat_ces.modules.quantity import PhysicalQuantity
from lat_ces.modules.pressure import PRESSURE
from lat_ces.modules.duct import DuctFrictionEngine, VISCOSITY_AIR


def test_reynolds_and_friction_factor():
    engine = DuctFrictionEngine()

    rho = PhysicalQuantity(1.2, DENSITY, 0.01)
    v = PhysicalQuantity(3.0, VELOCITY, 0.1)
    d_h = PhysicalQuantity(0.5, LENGTH, 0.01)
    mu = PhysicalQuantity(1.81e-5, VISCOSITY_AIR, 1e-7)

    re = engine.calculate_reynolds_number(rho, v, d_h, mu)
    assert re > 2300.0

    f = engine.estimate_friction_factor(re)
    assert 0.01 < f < 0.05


def test_friction_loss_calculation():
    engine = DuctFrictionEngine()

    f = 0.02
    length = PhysicalQuantity(10.0, LENGTH, 0.1)
    d_h = PhysicalQuantity(0.5, LENGTH, 0.01)
    rho = PhysicalQuantity(1.2, DENSITY, 0.01)
    v = PhysicalQuantity(4.0, VELOCITY, 0.1)

    dp = engine.calculate_friction_loss(f, length, d_h, rho, v)

    assert math.isclose(dp.value, 3.84, abs_tol=1e-2)
    assert dp.dimension == PRESSURE
    assert dp.uncertainty > 0