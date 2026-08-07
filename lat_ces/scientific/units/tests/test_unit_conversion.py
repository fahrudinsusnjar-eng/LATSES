"""
LAT-CES Scientific Core
Unit Conversion Verification Test (LAT-SCI-CORE-0014-EXT)
"""

import pytest

from lat_ces.scientific.units.dimension import LENGTH
from lat_ces.scientific.units.unit import METER, Unit


def test_millimeter_conversion_factor():
    millimeter = Unit(
        name="millimeter",
        symbol="mm",
        dimension=LENGTH,
        scale_factor=0.001,
    )

    # Provjera ustavnog faktora skale u odnosu na bazni SI metar
    assert millimeter.scale_factor == 0.001
    assert millimeter.dimension == LENGTH
