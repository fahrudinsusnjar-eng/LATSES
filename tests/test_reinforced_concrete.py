from lat_ces.structural.reinforced_concrete import (
    ConcreteMaterial,
    RCDesignActions,
    RCElementType,
    RCSection,
    Rebar,
    ReinforcedConcreteElement,
    ReinforcementSteel,
    StirrupLayout,
    evaluate_preliminary_rc_design,
    preliminary_flexural_steel_area,
)


def test_beam_preliminary_rebar_is_calculated_from_moment_and_section():
    section = RCSection(width_m=0.30, depth_m=0.50, cover_m=0.04, length_m=5.0)
    steel = ReinforcementSteel(grade="B500B", fyk_mpa=500.0)
    required = preliminary_flexural_steel_area(
        med_knm=80.0,
        section=section,
        steel=steel,
    )
    assert required is not None
    assert required > 0.0


def test_beam_reports_provided_layout_and_missing_transverse_design():
    element = ReinforcedConcreteElement(
        element_id="B1",
        element_type=RCElementType.BEAM,
        section=RCSection(width_m=0.30, depth_m=0.50, cover_m=0.04, length_m=5.0),
        concrete=ConcreteMaterial(grade="C25/30", fck_mpa=25.0),
        steel=ReinforcementSteel(grade="B500B", fyk_mpa=500.0),
        actions=RCDesignActions(med_knm=50.0, ved_kn=40.0),
        longitudinal_bars=[Rebar(diameter_mm=16.0, count=3, face="bottom", position="main")],
    )
    result = evaluate_preliminary_rc_design(element)
    assert result.required_as_mm2 is not None
    assert result.provided_as_mm2 > 0.0
    assert any("Transverse reinforcement" in item for item in result.findings)


def test_column_requires_axial_action_for_interaction_verification():
    element = ReinforcedConcreteElement(
        element_id="C1",
        element_type=RCElementType.COLUMN,
        section=RCSection(width_m=0.30, depth_m=0.30, cover_m=0.04, length_m=2.9),
        concrete=ConcreteMaterial(grade="C30/37", fck_mpa=30.0),
        steel=ReinforcementSteel(grade="B500B", fyk_mpa=500.0),
        actions=RCDesignActions(med_knm=20.0),
        longitudinal_bars=[Rebar(diameter_mm=16.0, count=4, position="vertical")],
        stirrups=[StirrupLayout(diameter_mm=8.0, spacing_mm=150.0, legs=4, zone="standard")],
    )
    result = evaluate_preliminary_rc_design(element)
    assert result.required_as_mm2 is not None
    assert any("NEd is required" in item for item in result.findings)
