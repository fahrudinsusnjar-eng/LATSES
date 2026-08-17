from lat_ces.structural.roof import RoofLayer, RoofLoadModel, RoofSpec


def test_roof_load_model_is_deterministic_and_reports_surface_load():
    roof = RoofSpec(
        shape="Dvovodni",
        support="Samo zidovi / serklaži",
        structural_system="Drvene grede",
        covering="Lim",
        length_m=10.0,
        width_m=8.0,
        rise_m=1.5,
        layers=[
            RoofLayer("Lim", mass_kg_m2=7.0),
            RoofLayer("Izolacija", thickness_m=0.20, density_kg_m3=30.0),
        ],
    )

    result = RoofLoadModel().evaluate(roof)

    assert result.area_m2 == 80.0
    assert result.load_kg_m2 == 13.0
    assert round(result.load_kn_m2, 6) == round(13.0 * 9.80665 / 1000.0, 6)
    assert result.total_mass_kg == 1040.0
    assert result.complete is True
    assert result.unresolved_layers == ()


def test_roof_input_never_invents_missing_material_data():
    try:
        RoofLayer("Nepoznat materijal", thickness_m=0.10)
    except ValueError as exc:
        assert "nema potvrđenu gustoću" in str(exc)
    else:
        raise AssertionError("RoofLayer must reject missing declared material data")
