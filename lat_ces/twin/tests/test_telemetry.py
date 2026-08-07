"""
LAT-CES Dynamic Twin Core
Sensor Telemetry Ingestion Tests (LAT-TWIN-CORE-0011-TEST)
"""

from datetime import datetime, timezone

import pytest

from lat_ces.scientific.units.quantity import Quantity
from lat_ces.scientific.units.unit import METER, SECOND
from lat_ces.twin.telemetry import TelemetryError, TelemetryIngester, TelemetryPacket


def test_telemetry_packet_creation():
    q = Quantity(22.5, METER, uncertainty=0.05)
    ts = datetime.now(timezone.utc)
    packet = TelemetryPacket(sensor_id="SENSOR-PLENUM-01", quantity=q, timestamp=ts)

    assert packet.sensor_id == "SENSOR-PLENUM-01"
    assert packet.quantity.value == 22.5
    assert packet.timestamp == ts


def test_telemetry_ingester_validation():
    ingester = TelemetryIngester()
    q = Quantity(101.3, METER, uncertainty=0.1)

    packet = TelemetryPacket(sensor_id="BARO-01", quantity=q, timestamp=datetime.now(timezone.utc))
    ingester.ingest(packet)

    latest = ingester.get_latest("BARO-01")
    assert latest.quantity.value == 101.3
