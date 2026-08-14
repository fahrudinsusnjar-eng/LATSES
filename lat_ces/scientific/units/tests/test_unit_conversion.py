"""
LAT-CES Scientific Core
Unit Conversion Verification Test (LAT-SCI-CORE-0014-EXT)

ADAPT-001: exercise canonical Unit/Dimension implementations.
"""

from lat_ces.core.dimensions import LENGTH, Unit


def test_millimeter_conversion_factor():
    millimeter = Unit(
        name="millimeter",
        symbol="mm",
        dimension=LENGTH,
        scale_factor=0.001,
    )

    assert millimeter.scale_factor == 0.001
    assert millimeter.dimension == LENGTH
