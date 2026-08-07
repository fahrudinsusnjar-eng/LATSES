from lat_ces.scientific.analysis.plenum import PlenumAnalysisEngine
from lat_ces.scientific.devices.device import create_pitot_tube
from lat_ces.scientific.dimensions.dimension import LENGTH, MASS, TIME
from lat_ces.scientific.equations.fluids import DynamicPressureEquation
from lat_ces.scientific.quantity import PhysicalQuantity
from lat_ces.scientific.units.units import Unit


def run_plenum_integration_demo() -> None:
    print("=" * 70)
    print(" LAT-CES SCIENTIFIC CORE: END-TO-END PLENUM DEMO")
    print(" Evaluation of dynamic pressure and plenum-channel safety")
    print("=" * 70)

    pitot_sensor = create_pitot_tube("Pitot-Prandtl Probe #HVAC-01")
    raw_velocity_reading = 18.5
    measured_velocity = pitot_sensor.measure(raw_velocity_reading)

    print("\n[1] MEASUREMENT DEVICE AND READING:")
    print(f"    Device:            {pitot_sensor.name} ({pitot_sensor.device_type})")
    print(f"    Raw reading:       {raw_velocity_reading:.2f} m/s")
    print(
        f"    Corrected (+/-u):  {measured_velocity.value:.2f} +/- "
        f"{measured_velocity.uncertainty:.3f} {measured_velocity.unit.symbol}"
    )
    print(
        f"    Relative uncertainty: "
        f"{measured_velocity.relative_uncertainty * 100:.2f}%"
    )

    kg_m3 = Unit("kilogram per cubic meter", "kg/m3", MASS / (LENGTH**3))
    air_density = PhysicalQuantity(1.204, 0.012, kg_m3)

    print("\n[2] FLUID PROPERTIES (AIR):")
    print(
        f"    Density (rho):     {air_density.value:.3f} +/- "
        f"{air_density.uncertainty:.3f} {air_density.unit.symbol}"
    )

    equation = DynamicPressureEquation()
    dynamic_pressure = equation.calculate(
        density=air_density,
        velocity=measured_velocity,
    )

    print("\n[3] EQUATION ENGINE (p_dyn = 0.5 * rho * v^2):")
    print(f"    Equation:           {equation.name}")
    print(
        f"    Dynamic pressure:   {dynamic_pressure.value:.2f} +/- "
        f"{dynamic_pressure.uncertainty:.2f} {dynamic_pressure.unit.symbol}"
    )
    print(
        f"    Relative uncertainty: "
        f"{dynamic_pressure.relative_uncertainty * 100:.2f}%"
    )

    pascal = Unit("pascal", "Pa", MASS / (LENGTH * (TIME**2)))
    structural_limit = PhysicalQuantity(220.0, 0.0, pascal)

    print("\n[4] PLENUM SAFETY-MARGIN EVALUATION:")
    print(f"    Structural limit:  {structural_limit.value:.1f} Pa")

    safety_report = PlenumAnalysisEngine.evaluate_limit(
        calculated=dynamic_pressure,
        limit=structural_limit,
        coverage_factor=2.0,
    )

    print(f"\n    >>> EVALUATION RESULT: [{safety_report.status.value}] <<<")
    print(
        f"    Expanded uncertainty (k=2.0): +/- "
        f"{safety_report.expanded_uncertainty:.2f} Pa"
    )
    print(
        f"    95% safety interval: {dynamic_pressure.value - safety_report.expanded_uncertainty:.2f} "
        f"Pa to {dynamic_pressure.value + safety_report.expanded_uncertainty:.2f} Pa"
    )
    print(f"    Nominal margin:     {safety_report.margin_to_limit:.2f} Pa")
    print(f"    Engineering report: {safety_report.message}")
    print("\n" + "=" * 70)


if __name__ == "__main__":
    run_plenum_integration_demo()