"""
Compatibility facade for the legacy LAT-CES plenum module.

The canonical implementation lives in ``lat_ces.scientific.plenum``.
This module intentionally contains no plenum calculation logic so the legacy
namespace cannot become a second implementation.
"""

from lat_ces.scientific.plenum import PlenumEngine

__all__ = ["PlenumEngine"]
