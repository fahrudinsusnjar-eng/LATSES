import pytest
from lat_ces.scientific.heat_exchanger import HeatExchangerNTUModel, HeatExchangerError


def test_ntu_effectiveness():
    model = HeatExchangerNTUModel()
    eff = model.compute_counterflow_effectiveness(ntu=1.5, capacity_ratio=0.8)
    assert 0.0 <= eff <= 1.0
