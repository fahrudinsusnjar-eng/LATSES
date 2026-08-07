from lat_ces.scientific.analysis.plenum import PlenumAnalysisEngine
from lat_ces.scientific.devices.device import create_pitot_tube
from lat_ces.scientific.dimensions.dimension import LENGTH, MASS, TIME
from lat_ces.scientific.equations.fluids import DynamicPressureEquation
from lat_ces.scientific.quantity import PhysicalQuantity
from lat_ces.scientific.reports.exporter import SKOReportExporter
from lat_ces.scientific.reports.pdf_generator import SKOPDFGenerator
from lat_ces.scientific.units.units import Unit


def run_plenum_workflow() -> None:
    print("=" * 70)
    print(" LAT-CES SCIENTIFIC CORE: INTEGRACIONI END-TO-END DEMO SCENARIJ")
    print(" Evaluacija Dinamickog Pritiska i Sigurnosti Plenumskog Kanala")
    print("=" * 70)

    pitot_sensor = create_pitot_tube("Pitot-Prandtl Sonda #HVAC-01")
    raw_velocity_reading = 18.5
    measured_velocity = pitot_sensor.measure(raw_velocity_reading)

    print("\n[1] MJERNI INSTRUMENT I OCITANJE:")
    print(f"    Uredjaj:            {pitot_sensor.name} ({pitot_sensor.device_type})")
    print(f"    Sirovo ocitanje:    {raw_velocity_reading:.2f} m/s")
    print(
        f"    Korigovano (+/-u):  {measured_velocity.value:.2f} +/- "
        f"{measured_velocity.uncertainty:.3f} {measured_velocity.unit.symbol}"
    )
    print(
        f"    Rel. neodredjenost: {measured_velocity.relative_uncertainty * 100:.2f}%"
    )

    kg_m3 = Unit("kilogram per cubic meter", "kg/m3", MASS / (LENGTH**3))
    air_density = PhysicalQuantity(1.204, 0.012, kg_m3)

    print("\n[2] SVOJSTVA FLUIDA (ZRAK):")
    print(
        f"    Gustoca (rho):      {air_density.value:.3f} +/- "
        f"{air_density.uncertainty:.3f} {air_density.unit.symbol}"
    )

    equation = DynamicPressureEquation()
    dynamic_pressure = equation.calculate(density=air_density, velocity=measured_velocity)

    print("\n[3] PRORACUN U EQUATION ENGINE-U (p_dyn = 0.5 * rho * v^2):")
    print(f"    Primijenjena jednacina: {equation.name}")
    print(
        f"    Izracunat pritisak:     {dynamic_pressure.value:.2f} +/- "
        f"{dynamic_pressure.uncertainty:.2f} {dynamic_pressure.unit.symbol}"
    )
    print(
        f"    Propagirana rel. neodr.: "
        f"{dynamic_pressure.relative_uncertainty * 100:.2f}%"
    )

    pascal = Unit("pascal", "Pa", MASS / (LENGTH * (TIME**2)))
    structural_limit = PhysicalQuantity(220.0, 0.0, pascal)

    print("\n[4] EVALUACIJA SIGURNOSNIH MARGINA PLENUMA:")
    print(f"    Strukturalni limit plenuma: {structural_limit.value:.1f} Pa")

    safety_report = PlenumAnalysisEngine.evaluate_limit(
        calculated=dynamic_pressure,
        limit=structural_limit,
        coverage_factor=2.0,
    )

    lower = dynamic_pressure.value - safety_report.expanded_uncertainty
    upper = dynamic_pressure.value + safety_report.expanded_uncertainty
    print(f"\n    >>> REZULTAT EVALUACIJE: [{safety_report.status.value}] <<<")
    print(
        f"    Prosirena neodredjenost (k=2.0, 95%): "
        f"+/-{safety_report.expanded_uncertainty:.2f} Pa"
    )
    print(f"    Sigurnosni raspon: {lower:.2f} Pa do {upper:.2f} Pa")
    print(f"    Nom. margina do limita: {safety_report.margin_to_limit:.2f} Pa")
    print(f"    Inzenjerski izvjestaj: {safety_report.message}")

    exporter = SKOReportExporter(
        project_name="LAT-CES Plenum Vent Analysis",
        engineer_name="fahrudin Susnjar",
        plenum_id="PLENUM-MAIN-01",
        safety_report=safety_report,
        inputs={"velocity": measured_velocity, "density": air_density},
        device=pitot_sensor,
        equation_name=equation.name,
    )

    with open("demo_report.json", "w", encoding="utf-8") as file:
        file.write(exporter.to_json())

    with open("demo_report.md", "w", encoding="utf-8") as file:
        file.write(exporter.to_markdown())

    SKOPDFGenerator.generate_pdf(exporter, "demo_report.pdf")

    print("\n[5] SKO IZVJESTAJ USPJESNO GENERISAN:")
    print("    JSON Audit Trail: demo_report.json")
    print("    Markdown Certifikat: demo_report.md")
    print("    Sluzbeni PDF Certifikat: demo_report.pdf")
    print("\n" + "=" * 70)


if __name__ == "__main__":
    run_plenum_workflow()