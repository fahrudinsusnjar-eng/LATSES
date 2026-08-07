"""
LAT-CES Dynamic Twin Core
Sensor Telemetry Ingestion Reference Implementation (LAT-TWIN-CORE-0011)
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional

from lat_ces.scientific.units.quantity import Quantity


class TelemetryError(Exception):
    """Base exception for Telemetry operations."""

    pass


@dataclass(frozen=True)
class TelemetryPacket:
    """
    Represents an immutable, time-stamped physical measurement packet from a sensor.
    """

    sensor_id: str
    quantity: Quantity
    timestamp: datetime

    def __post_init__(self):
        if not self.sensor_id:
            raise TelemetryError("Telemetry packet requires a valid sensor_id.")
        if not isinstance(self.quantity, Quantity):
            raise TelemetryError("Telemetry packet payload must be a valid Quantity.")
        if not isinstance(self.timestamp, datetime):
            raise TelemetryError("Telemetry packet requires a valid datetime timestamp.")


class TelemetryIngester:
    """
    Manages ingestion, caching, and retrieval of live physical sensor streams.
    """

    def __init__(self):
        self._stream_cache: Dict[str, TelemetryPacket] = {}

    def ingest(self, packet: TelemetryPacket) -> None:
        """Ingests and validates incoming telemetry packet."""
        if not isinstance(packet, TelemetryPacket):
            raise TelemetryError("Invalid telemetry packet type.")
        self._stream_cache[packet.sensor_id] = packet

    def get_latest(self, sensor_id: str) -> TelemetryPacket:
        """Retrieves the latest telemetry packet for a given sensor."""
        if sensor_id not in self._stream_cache:
            raise TelemetryError(f"No telemetry data found for sensor: {sensor_id}")
        return self._stream_cache[sensor_id]
