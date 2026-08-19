from lat_ces.building_model.example_model import make_small_reference_house
from lat_ces.building_model.integration import analyze_building
from lat_ces.building_model.validation import Status


def test_small_reference_house_drives_all_first_order_engines():
    model = make_small_reference_house()
    report = analyze_building(model)

    assert model.total_volume_m3() == 448.0
    assert report.airflow.air_changes_per_hour == 0.85
    assert report.airflow.velocity_m_s == 0.05
    assert report.airflow.human_zone_ok is True
    assert report.airflow.flow_m3_h == 380.8

    assert report.water.velocity_m_s > 0.0
    assert report.heating.required_w > 0.0
    assert report.heating.emitter_type == "underfloor"

    assert report.validation
    assert all(result.status is Status.PASS for result in report.validation)
