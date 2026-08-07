"""
LAT-CES Storage Core
Time-Series Storage Engine Reference Implementation (LAT-DATA-CORE-0011)
"""

from datetime import datetime
from typing import List, Dict

from lat_ces.twin.telemetry import TelemetryPacket


class StorageError(Exception):
    """Base exception for Time-Series Storage operations."""

    pass


class TimeSeriesStorage:
    """
    In-memory / Persistent store for timestamped physical telemetry streams.
    """

    def __init__(self):
        self._store: Dict[str, List[TelemetryPacket]] = {}

    def save(self, packet: TelemetryPacket) -> None:
        """Saves a telemetry packet into the chronological storage stream."""
        if not isinstance(packet, TelemetryPacket):
            raise StorageError("Invalid packet type for storage.")

        if packet.sensor_id not in self._store:
            self._store[packet.sensor_id] = []

        self._store[packet.sensor_id].append(packet)
        # Keep sorted by timestamp
        self._store[packet.sensor_id].sort(key=lambda p: p.timestamp)

    def query(self, sensor_id: str, start_time: datetime, end_time: datetime) -> List[TelemetryPacket]:
        """Queries telemetry packets for a sensor within a given time interval."""
        if sensor_id not in self._store:
            return []

        packets = self._store[sensor_id]
        return [p for p in packets if start_time <= p.timestamp <= end_time]
