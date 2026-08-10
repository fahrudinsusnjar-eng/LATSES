import pytest

from lat_ces.scientific.analysis.plenum import PlenumAnalysisEngine, SafetyStatus
from lat_ces.scientific.dimensions.dimension import LENGTH, MASS, TIME
from lat_ces.scientific.equations.engine import DimensionalityError
from lat_ces.scientific.quantities.quantity import PhysicalQuantity
from lat_ces.scientific.units.units import Unit


def test_plenum_safety_status_safe():
    pascal = Unit("pascal", "Pa", MASS / (LENGTH * (TIME**2)))
    calc_p = PhysicalQuantity(300.0, 10.0, pascal)
    limit_p = PhysicalQuantity(500.0, 0.0, pascal)

    report = PlenumAnalysisEngine.evaluate_limit(calc_p, limit_p)

    assert report.status == SafetyStatus.SAFE
    assert report.margin_to_limit == pytest.approx(200.0)


def test_plenum_safety_status_metrological_risk():
    pascal = Unit("pascal", "Pa", MASS / (LENGTH * (TIME**2)))
    calc_p = PhysicalQuantity(490.0, 10.0, pascal)
    limit_p = PhysicalQuantity(500.0, 0.0, pascal)

    report = PlenumAnalysisEngine.evaluate_limit(calc_p, limit_p)

    assert report.status == SafetyStatus.METROLOGICAL_RISK
    assert "METROLOŠKI RIZIK" in report.message


def test_plenum_safety_status_critical():
    pascal = Unit("pascal", "Pa", MASS / (LENGTH * (TIME**2)))
    calc_p = PhysicalQuantity(520.0, 5.0, pascal)
    limit_p = PhysicalQuantity(500.0, 0.0, pascal)

    report = PlenumAnalysisEngine.evaluate_limit(calc_p, limit_p)

    assert report.status == SafetyStatus.CRITICAL_EXCEEDED


def test_plenum_analysis_dimensionality_mismatch():
    pascal = Unit("pascal", "Pa", MASS / (LENGTH * (TIME**2)))
    meter = Unit("meter", "m", LENGTH)
    calc_p = PhysicalQuantity(300.0, 10.0, pascal)
    limit_m = PhysicalQuantity(500.0, 0.0, meter)

    with pytest.raises(DimensionalityError):
        PlenumAnalysisEngine.evaluate_limit(calc_p, limit_m)