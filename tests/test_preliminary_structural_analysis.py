from lat_ces.structural.preliminary_analysis import (
    FloorAction,
    PreliminaryStructuralAnalysis,
    VerticalElement,
)


def test_vertical_load_path_accumulates_to_foundation() -> None:
    analysis = PreliminaryStructuralAnalysis()
    analysis.add_floor_action(FloorAction("Prizemlje", 80.0, permanent_kn_m2=4.0, imposed_kn_m2=2.0))
    analysis.add_floor_action(FloorAction("Sprat", 80.0, permanent_kn_m2=3.0, imposed_kn_m2=2.0))
    analysis.add_floor_action(FloorAction("Krov", 80.0, permanent_kn_m2=1.5, snow_kn_m2=1.0))
    analysis.add_vertical_element(VerticalElement("W-G-01", "load-bearing-wall", "Prizemlje"))
    analysis.add_vertical_element(VerticalElement("W-1-01", "load-bearing-wall", "Sprat"))
    analysis.add_vertical_element(VerticalElement("W-R-01", "load-bearing-wall", "Krov"))

    result = analysis.evaluate()

    assert result.status == "READY_PRELIMINARY"
    assert result.load_path[-1].permanent_kn == 680.0
    assert result.load_path[-1].imposed_kn == 320.0
    assert result.load_path[-1].snow_kn == 80.0
    assert result.total_gravity_kn == 1080.0
    assert result.foundation_reactions[0].total_kn == 1080.0


def test_missing_load_carrier_is_explicit_input_required() -> None:
    analysis = PreliminaryStructuralAnalysis()
    analysis.add_floor_action(FloorAction("Sprat", 80.0, permanent_kn_m2=3.0))

    result = analysis.evaluate()

    assert result.status == "INPUT_REQUIRED"
    assert "No declared vertical load carrier at level: Sprat" in result.findings
