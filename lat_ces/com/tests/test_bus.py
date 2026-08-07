"""
LAT-CES Communication Core
Async Event Bus Verification Tests (LAT-COM-CORE-0011-TEST)
"""

import pytest

from lat_ces.com.bus import EventBus


def test_event_subscription_and_publishing():
    bus = EventBus()
    received_events = []

    def callback(data):
        received_events.append(data)

    bus.subscribe("SYSTEM_ALERT", callback)
    bus.publish("SYSTEM_ALERT", {"severity": "HIGH"})

    assert len(received_events) == 1
    assert received_events[0]["severity"] == "HIGH"
