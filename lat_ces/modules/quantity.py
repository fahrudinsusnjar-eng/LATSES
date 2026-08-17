"""Compatibility import for the canonical PhysicalQuantity implementation.

Legacy module callers may continue constructing quantities with a Dimension;
the canonical implementation adapts that form to a registered SI Unit.
"""

from lat_ces.scientific.quantity.quantity import PhysicalQuantity

__all__ = ["PhysicalQuantity"]
