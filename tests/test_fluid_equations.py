import math

import pytest

from lat_ces.scientific.dimensions.dimension import (
    DIMENSIONLESS,
    LENGTH,
    MASS,
    TEMPERATURE,
    TIME,
)
from lat_ces.scientific.equations.engine import (
    DimensionalityError,
    PhysicalDomainError,
)
from lat_ces.scientific.equations.fluids import (
    BiotNumberEquation,
    ContinuityEquation,
    FourierNumberEquation,
    HEAT_TRANSFER_COEFFICIENT,
    MachNumberEquation,
    MassFlowEquation,
    NusseltNumberEquation,
    PlenumPressureDropEquation,
    PrandtlNumberEquation,
    ReynoldsNumberEquation,
    VolumetricFlowEquation,
)
from lat_ces.scientific.quantities.quantity import PhysicalQuantity
from lat_ces.scientific.units.units import Unit


def test_continuity_equation_with_uncertainty():
    m2 = Unit("square meter", "m²", LENGTH**2)
    m_s = Unit("meter per second", "m/s", LENGTH / TIME)
    area = PhysicalQuantity(2.0, 0.1, m2)
    velocity = PhysicalQuantity(10.0, 0.2, m_s)

    flow = ContinuityEquation().calculate(area=area, velocity=velocity)

    assert flow.value == pytest.approx(20.0)
    assert flow.unit.symbol == "m²·m/s"
    expected_relative_uncertainty = math.sqrt((0.1 / 2.0) ** 2 + (0.2 / 10.0) ** 2)
    assert flow.relative_uncertainty == pytest.approx(expected_relative_uncertainty)


def test_volumetric_flow_equation_evaluate_alias():
    m2 = Unit("square meter", "m²", LENGTH**2)
    m_s = Unit("meter per second", "m/s", LENGTH / TIME)
    area = PhysicalQuantity(2.0, 0.1, m2)
    velocity = PhysicalQuantity(10.0, 0.2, m_s)

    result = VolumetricFlowEquation().evaluate(area=area, velocity=velocity)

    assert result.value == pytest.approx(20.0)
    assert result.unit.symbol == "m²·m/s"


def test_mass_flow_equation_evaluate_alias():
    rho_u = Unit("kilogram per cubic meter", "kg/m3", MASS / (LENGTH**3))
    q_u = Unit("cubic meter per second", "m3/s", LENGTH**3 / TIME)
    density = PhysicalQuantity(1.2, 0.012, rho_u)
    flow = PhysicalQuantity(2.0, 0.05, q_u)

    result = MassFlowEquation().evaluate(density=density, volumetric_flow=flow)

    assert result.value == pytest.approx(2.4)
    assert result.unit.symbol == "kg/s"
    expected_relative_uncertainty = math.sqrt((0.012 / 1.2) ** 2 + (0.05 / 2.0) ** 2)
    assert result.relative_uncertainty == pytest.approx(expected_relative_uncertainty)


def test_continuity_equation_rejects_wrong_area_dimension():
    meter = Unit("meter", "m", LENGTH)
    m_s = Unit("meter per second", "m/s", LENGTH / TIME)
    wrong_area = PhysicalQuantity(2.0, 0.1, meter)
    velocity = PhysicalQuantity(10.0, 0.2, m_s)

    with pytest.raises(DimensionalityError):
        ContinuityEquation().calculate(area=wrong_area, velocity=velocity)


def test_continuity_equation_rejects_negative_velocity():
    m2 = Unit("square meter", "m²", LENGTH**2)
    m_s = Unit("meter per second", "m/s", LENGTH / TIME)
    area = PhysicalQuantity(2.0, 0.1, m2)
    velocity = PhysicalQuantity(-1.0, 0.1, m_s)

    with pytest.raises(PhysicalDomainError):
        ContinuityEquation().calculate(area=area, velocity=velocity)


def test_reynolds_number_equation():
    density_unit = Unit(
        "kilogram per cubic meter",
        "kg/m3",
        MASS / (LENGTH**3),
    )
    velocity_unit = Unit(
        "meter per second",
        "m/s",
        LENGTH / TIME,
    )
    length_unit = Unit(
        "meter",
        "m",
        LENGTH,
    )
    viscosity_unit = Unit(
        "pascal second",
        "Pa·s",
        MASS / (LENGTH * TIME),
    )

    density = PhysicalQuantity(1.2, 0.012, density_unit)
    velocity = PhysicalQuantity(10.0, 0.1, velocity_unit)
    characteristic_length = PhysicalQuantity(
        0.1,
        0.001,
        length_unit,
    )
    dynamic_viscosity = PhysicalQuantity(
        1.8e-5,
        1.8e-7,
        viscosity_unit,
    )

    result = ReynoldsNumberEquation().calculate(
        density=density,
        velocity=velocity,
        characteristic_length=characteristic_length,
        dynamic_viscosity=dynamic_viscosity,
    )

    assert result.value == pytest.approx(
        (1.2 * 10.0 * 0.1) / 1.8e-5
    )
    assert result.unit.symbol == "-"
    assert result.dimension == DIMENSIONLESS
    assert result.uncertainty > 0.0


def test_reynolds_number_rejects_non_positive_viscosity():
    density_unit = Unit(
        "kilogram per cubic meter",
        "kg/m3",
        MASS / (LENGTH**3),
    )
    velocity_unit = Unit(
        "meter per second",
        "m/s",
        LENGTH / TIME,
    )
    length_unit = Unit(
        "meter",
        "m",
        LENGTH,
    )
    viscosity_unit = Unit(
        "pascal second",
        "Pa·s",
        MASS / (LENGTH * TIME),
    )

    with pytest.raises(PhysicalDomainError):
        ReynoldsNumberEquation().calculate(
            density=PhysicalQuantity(1.2, 0.0, density_unit),
            velocity=PhysicalQuantity(10.0, 0.0, velocity_unit),
            characteristic_length=PhysicalQuantity(0.1, 0.0, length_unit),
            dynamic_viscosity=PhysicalQuantity(
                0.0,
                0.0,
                viscosity_unit,
            ),
        )


def test_mach_number_equation():
    velocity_unit = Unit(
        "meter per second",
        "m/s",
        LENGTH / TIME,
    )

    velocity = PhysicalQuantity(
        340.0,
        3.4,
        velocity_unit,
    )

    speed_of_sound = PhysicalQuantity(
        340.0,
        1.7,
        velocity_unit,
    )

    result = MachNumberEquation().calculate(
        velocity=velocity,
        speed_of_sound=speed_of_sound,
    )

    assert result.value == pytest.approx(1.0)
    assert result.unit.symbol == "-"
    assert result.dimension == DIMENSIONLESS
    assert result.uncertainty > 0.0


def test_mach_number_rejects_non_positive_speed_of_sound():
    velocity_unit = Unit(
        "meter per second",
        "m/s",
        LENGTH / TIME,
    )

    with pytest.raises(PhysicalDomainError):
        MachNumberEquation().calculate(
            velocity=PhysicalQuantity(
                100.0,
                0.0,
                velocity_unit,
            ),
            speed_of_sound=PhysicalQuantity(
                0.0,
                0.0,
                velocity_unit,
            ),
        )


def test_prandtl_number_equation():
    """Pr = nu / alpha should produce a dimensionless result."""
    equation = PrandtlNumberEquation()

    nu = PhysicalQuantity(
        1.5e-5,
        0.0,
        Unit("m2/s", "m²/s", LENGTH**2 / TIME),
    )

    alpha = PhysicalQuantity(
        2.2e-5,
        0.0,
        Unit("m2/s", "m²/s", LENGTH**2 / TIME),
    )

    result = equation.calculate(
        kinematic_viscosity=nu,
        thermal_diffusivity=alpha,
    )

    assert result.value == pytest.approx(1.5e-5 / 2.2e-5)
    assert result.dimension == DIMENSIONLESS


def test_prandtl_number_rejects_wrong_dimensions():
    """Prandtl number inputs must both have dimensions L²/T."""
    equation = PrandtlNumberEquation()

    velocity = PhysicalQuantity(
        10.0,
        0.0,
        Unit("m/s", "m/s", LENGTH / TIME),
    )

    alpha = PhysicalQuantity(
        2.2e-5,
        0.0,
        Unit("m2/s", "m²/s", LENGTH**2 / TIME),
    )

    with pytest.raises(DimensionalityError):
        equation.calculate(
            kinematic_viscosity=velocity,
            thermal_diffusivity=alpha,
        )


def test_nusselt_number_equation():
    """Nu = h * L / k."""
    equation = NusseltNumberEquation()

    heat_transfer_coefficient = PhysicalQuantity(
        100.0,
        0.0,
        Unit(
            "W/(m2*K)",
            "W/(m²·K)",
            MASS / (TIME**3 * TEMPERATURE),
        ),
    )

    characteristic_length = PhysicalQuantity(
        0.1,
        0.0,
        Unit("m", "m", LENGTH),
    )

    thermal_conductivity = PhysicalQuantity(
        0.5,
        0.0,
        Unit(
            "W/(m*K)",
            "W/(m·K)",
            MASS * LENGTH / (TIME**3 * TEMPERATURE),
        ),
    )

    result = equation.calculate(
        heat_transfer_coefficient=heat_transfer_coefficient,
        characteristic_length=characteristic_length,
        thermal_conductivity=thermal_conductivity,
    )

    assert result.value == pytest.approx(20.0)
    assert result.dimension == DIMENSIONLESS


def test_nusselt_number_rejects_wrong_dimensions():
    equation = NusseltNumberEquation()

    velocity = PhysicalQuantity(
        10.0,
        0.0,
        Unit("m/s", "m/s", LENGTH / TIME),
    )

    characteristic_length = PhysicalQuantity(
        0.1,
        0.0,
        Unit("m", "m", LENGTH),
    )

    thermal_conductivity = PhysicalQuantity(
        0.5,
        0.0,
        Unit(
            "W/(m*K)",
            "W/(m·K)",
            MASS * LENGTH / (TIME**3 * TEMPERATURE),
        ),
    )

    with pytest.raises(DimensionalityError):
        equation.calculate(
            heat_transfer_coefficient=velocity,
            characteristic_length=characteristic_length,
            thermal_conductivity=thermal_conductivity,
        )


def test_biot_number_equation():
    """Bi = h * Lc / k."""
    equation = BiotNumberEquation()

    heat_transfer_coefficient = PhysicalQuantity(
        100.0,
        0.0,
        Unit(
            "W/(m2*K)",
            "W/(m²·K)",
            MASS / (TIME**3 * TEMPERATURE),
        ),
    )

    characteristic_length = PhysicalQuantity(
        0.1,
        0.0,
        Unit("m", "m", LENGTH),
    )

    thermal_conductivity = PhysicalQuantity(
        0.5,
        0.0,
        Unit(
            "W/(m*K)",
            "W/(m·K)",
            MASS * LENGTH / (TIME**3 * TEMPERATURE),
        ),
    )

    result = equation.calculate(
        heat_transfer_coefficient=heat_transfer_coefficient,
        characteristic_length=characteristic_length,
        thermal_conductivity=thermal_conductivity,
    )

    assert result.value == pytest.approx(20.0)
    assert result.dimension == DIMENSIONLESS


def test_biot_number_rejects_wrong_dimensions():
    """Biot number must reject invalid physical dimensions."""
    equation = BiotNumberEquation()

    velocity = PhysicalQuantity(
        10.0,
        0.0,
        Unit("m/s", "m/s", LENGTH / TIME),
    )

    characteristic_length = PhysicalQuantity(
        0.1,
        0.0,
        Unit("m", "m", LENGTH),
    )

    thermal_conductivity = PhysicalQuantity(
        0.5,
        0.0,
        Unit(
            "W/(m*K)",
            "W/(m·K)",
            MASS * LENGTH / (TIME**3 * TEMPERATURE),
        ),
    )

    with pytest.raises(DimensionalityError):
        equation.calculate(
            heat_transfer_coefficient=velocity,
            characteristic_length=characteristic_length,
            thermal_conductivity=thermal_conductivity,
        )


def test_fourier_number_equation():
    """Fo = alpha * t / Lc²."""
    equation = FourierNumberEquation()

    thermal_diffusivity = PhysicalQuantity(
        1.0e-5,
        0.0,
        Unit(
            "m2/s",
            "m²/s",
            LENGTH**2 / TIME,
        ),
    )

    time = PhysicalQuantity(
        100.0,
        0.0,
        Unit("s", "s", TIME),
    )

    characteristic_length = PhysicalQuantity(
        0.1,
        0.0,
        Unit("m", "m", LENGTH),
    )

    result = equation.calculate(
        thermal_diffusivity=thermal_diffusivity,
        time=time,
        characteristic_length=characteristic_length,
    )

    assert result.value == pytest.approx(0.1)
    assert result.dimension == DIMENSIONLESS


def test_fourier_number_rejects_wrong_dimensions():
    """Fourier number must reject invalid input dimensions."""
    equation = FourierNumberEquation()

    velocity = PhysicalQuantity(
        10.0,
        0.0,
        Unit("m/s", "m/s", LENGTH / TIME),
    )

    time = PhysicalQuantity(
        100.0,
        0.0,
        Unit("s", "s", TIME),
    )

    characteristic_length = PhysicalQuantity(
        0.1,
        0.0,
        Unit("m", "m", LENGTH),
    )

    with pytest.raises(DimensionalityError):
        equation.calculate(
            thermal_diffusivity=velocity,
            time=time,
            characteristic_length=characteristic_length,
        )


def test_fourier_number_length_squared_dimension():
    """Squaring a length must produce an area dimension."""
    length = PhysicalQuantity(
        0.1,
        0.0,
        Unit("m", "m", LENGTH),
    )

    squared = length ** 2

    assert squared.value == pytest.approx(0.01)
    assert squared.dimension == LENGTH**2


def test_plenum_pressure_drop_equation_calculation():
    pascal = Unit("pascal", "Pa", MASS / (LENGTH * (TIME**2)))
    zeta = PhysicalQuantity(1.8, 0.05, Unit("dimensionless", "-", DIMENSIONLESS))
    dynamic_pressure = PhysicalQuantity(120.0, 3.0, pascal)

    pressure_drop = PlenumPressureDropEquation().calculate(
        resistance_coefficient=zeta,
        dynamic_pressure=dynamic_pressure,
    )

    assert pressure_drop.value == pytest.approx(216.0)
    assert pressure_drop.unit.symbol == "Pa"


def test_plenum_pressure_drop_equation_rejects_invalid_domain():
    pascal = Unit("pascal", "Pa", MASS / (LENGTH * (TIME**2)))
    zeta = PhysicalQuantity(-0.1, 0.0, Unit("dimensionless", "-", DIMENSIONLESS))
    dynamic_pressure = PhysicalQuantity(120.0, 3.0, pascal)

    with pytest.raises(PhysicalDomainError):
        PlenumPressureDropEquation().calculate(
            resistance_coefficient=zeta,
            dynamic_pressure=dynamic_pressure,
        )