"""
LAT-CES Communication Core
Async Event Bus Reference Implementation (LAT-COM-CORE-0011)
"""

from typing import Callable, Dict, List, Any


class EventBus:
    """
    Implements a simple Pub/Sub mechanism for internal system communication.
    """

    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, callback: Callable[[Any], None]) -> None:
        """Subscribes a callback function to a specific event type."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)

    def publish(self, event_type: str, data: Any) -> None:
        """Publishes event data to all registered subscribers."""
        if event_type in self._subscribers:
            for callback in self._subscribers[event_type]:
                callback(data)
