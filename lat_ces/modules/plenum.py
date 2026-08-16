"""
Compatibility facade for the legacy LAT-CES plenum module.

The canonical implementation lives in ``lat_ces.scientific.plenum`` and the
canonical derived dimensions live in ``lat_ces.core.dimensions``.  This module
intentionally contains no plenum calculation logic so the legacy namespace
cannot become a second implementation.
"""

from lat_ces.core.dimensions import AREA, DENSITY, FLOW_RATE, MASS_FLOW
from lat_ces.scientific.plenum import PlenumEngine

__all__ = ["PlenumEngine", "AREA", "DENSITY", "FLOW_RATE", "MASS_FLOW"]
