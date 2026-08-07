import math
from lat_ces.modules.acoustics import AcousticsEngine, P_REF


def test_pressure_to_db():
    assert math.isclose(AcousticsEngine.pressure_to_db(P_REF), 0.0, abs_tol=1e-5)

    db_1pa = AcousticsEngine.pressure_to_db(1.0)
    assert math.isclose(db_1pa, 93.979, abs_tol=1e-3)


def test_combine_noise_levels():
    combined = AcousticsEngine.combine_noise_levels([50.0, 50.0])
    assert math.isclose(combined, 53.01, abs_tol=0.01)


def test_noise_acceptability():
    assert AcousticsEngine.is_noise_acceptable(40.0, max_limit_db=45.0) is True
    assert AcousticsEngine.is_noise_acceptable(50.0, max_limit_db=45.0) is False