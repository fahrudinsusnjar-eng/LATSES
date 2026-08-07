"""
LAT-CES Storage Core
Time-Series Storage Engine Verification Tests (LAT-DATA-CORE-0011-TEST)
"""

from datetime import datetime, timedelta, timezone

import pytest

from lat_ces.data.timeseries import StorageError, TimeSeriesStorage
from lat_ces.scientific.units.quantity import Quantity
from lat_ces.scientific.units.unit import METER
from lat_ces.twin.telemetry import TelemetryPacket


def test_timeseries_storage_and_query():
    storage = TimeSeriesStorage()
    now = datetime.now(timezone.utc)

    q1 = Quantity(10.0, METER, uncertainty=0.1)
    q2 = Quantity(12.0, METER, uncertainty=0.1)

    packet1 = TelemetryPacket(sensor_id="S1", quantity=q1, timestamp=now - timedelta(minutes=5))
    packet2 = TelemetryPacket(sensor_id="S1", quantity=q2, timestamp=now)

    storage.save(packet1)
    storage.save(packet2)

    results = storage.query("S1", start_time=now - timedelta(minutes=10), end_time=now + timedelta(minutes=1))
    assert len(results) == 2
    assert results[1].quantity.value == 12.0
