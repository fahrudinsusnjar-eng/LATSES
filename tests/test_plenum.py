import pytest
import math
from lat_ces.core.dimensions import Dimension, AREA as CORE_AREA, FLOW_RATE as CORE_FLOW_RATE, DENSITY as CORE_DENSITY, MASS_FLOW as CORE_MASS_FLOW
from lat_ces.modules.quantity import PhysicalQuantity
from lat_ces.modules.plenum import PlenumEngine, AREA, FLOW_RATE, DENSITY, MASS_FLOW


def test_plenum_dimensions_are_canonical_core_objects():
    assert AREA is CORE_AREA
    assert FLOW_RATE is CORE_FLOW_RATE
    assert DENSITY is CORE_DENSITY
    assert MASS_FLOW is CORE_MASS_FLOW


def test_plenum_flow_calculation():
    engine = PlenumEngine()

    # Površina poprečnog presjeka plenuma: A = 2.0 ± 0.05 m²
    area = PhysicalQuantity(2.0, AREA, 0.05)
    # Izmjerena brzina zraka: v = 3.0 ± 0.1 m/s
    velocity = PhysicalQuantity(3.0, Dimension(L=1, T=-1), 0.1)

    # Q = A * v = 6.0 m³/s
    q = engine.calculate_airflow(area, velocity)

    assert q.value == 6.0
    assert q.dimension == FLOW_RATE
    assert q.uncertainty > 0


def test_plenum_mass_flow_calculation():
    engine = PlenumEngine()

    # Gustoća zraka: rho = 1.2 ± 0.01 kg/m³
    density = PhysicalQuantity(1.2, DENSITY, 0.01)
    # Protok: Q = 5.0 ± 0.1 m³/s
    q = PhysicalQuantity(5.0, FLOW_RATE, 0.1)

    # m_dot = rho * Q = 6.0 kg/s
    m_dot = engine.calculate_mass_flow(density, q)

    assert m_dot.value == 6.0
    assert m_dot.dimension == MASS_FLOW
