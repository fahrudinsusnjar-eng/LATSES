import pytest

from lat_ces.scientific.dimensions.dimension import LENGTH, TIME, VELOCITY
from lat_ces.scientific.equation import (
    DimensionalityError,
    PhysicalDomainError,
    PhysicalEquation,
)
from lat_ces.scientific.quantity import PhysicalQuantity
from lat_ces.scientific.units.units import Unit


class SpeedEquation(PhysicalEquation):
    @property
    def name(self):
        return "Speed equation"

    @property
    def expected_dimensions(self):
        return {"distance": LENGTH, "duration": TIME}

    def _check_physical_domain(self, kwargs):
        if kwargs["duration"].value <= 0.0:
            raise PhysicalDomainError("Duration must be positive.")

    def _compute(self, kwargs):
        return kwargs["distance"] / kwargs["duration"]


def make_quantities():
    meter = Unit("meter", "m", LENGTH)
    second = Unit("second", "s", TIME)
    return (
        PhysicalQuantity(100.0, 0.0, meter),
        PhysicalQuantity(10.0, 0.0, second),
        PhysicalQuantity(1.0, 0.0, meter),
    )


def test_scientific_equation_calculates_valid_inputs():
    distance, duration, _ = make_quantities()

    result = SpeedEquation().calculate(distance=distance, duration=duration)

    assert result.value == 10.0
    assert result.unit.dimension == VELOCITY


def test_scientific_equation_rejects_missing_and_wrong_type_inputs():
    distance, _, _ = make_quantities()
    equation = SpeedEquation()

    with pytest.raises(ValueError):
        equation.calculate(distance=distance)
    with pytest.raises(TypeError):
        equation.calculate(distance=distance, duration=10.0)


def test_scientific_equation_rejects_wrong_dimensions():
    distance, _, wrong_dimension = make_quantities()

    with pytest.raises(DimensionalityError):
        SpeedEquation().calculate(distance=distance, duration=wrong_dimension)


def test_scientific_equation_checks_physical_domain():
    distance, _, _ = make_quantities()
    meter = Unit("meter", "m", LENGTH)
    zero_duration = PhysicalQuantity(0.0, 0.0, Unit("second", "s", TIME))

    with pytest.raises(PhysicalDomainError):
        SpeedEquation().calculate(distance=distance, duration=zero_duration)