import pytest
from lat_ces.core.dimensions import LENGTH, TIME, VELOCITY, MASS, FORCE
from lat_ces.modules.quantity import PhysicalQuantity
from lat_ces.modules.equation import PhysicalEquation

def test_equation_valid_calculation():
    speed_eq = PhysicalEquation(
        name="Brzina",
        expected_dimension=VELOCITY,
        formula=lambda s, t: s / t
    )

    s = PhysicalQuantity(100.0, LENGTH, 1.0)
    t = PhysicalQuantity(10.0, TIME, 0.2)

    v = speed_eq.compute(s=s, t=t)
    assert v.value == 10.0
    assert v.dimension == VELOCITY

def test_equation_dimension_mismatch():
    faulty_eq = PhysicalEquation(
        name="Pogrešna Sila",
        expected_dimension=FORCE,
        formula=lambda s, t: s / t
    )

    s = PhysicalQuantity(100.0, LENGTH, 1.0)
    t = PhysicalQuantity(10.0, TIME, 0.2)

    with pytest.raises(ValueError):
        _ = faulty_eq.compute(s=s, t=t)