import pytest
from lat_ces.scientific.mass_balance import MassBalanceModel, MassBalanceError


def test_mass_conservation_check():
    model = MassBalanceModel()
    inflows = [1.2, 0.8]
    outflows = [1.0, 0.9, 0.1]
    is_balanced = model.verify_conservation(inflows, outflows, tolerance=1e-3)
    assert is_balanced is True
