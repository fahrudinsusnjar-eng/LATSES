import ast
import inspect
from pathlib import Path
from types import SimpleNamespace

from lat_ces.master_pipeline import LATCESMasterSystem


REPO_ROOT = Path(__file__).resolve().parents[1]
MASTER_PATH = REPO_ROOT / "lat_ces" / "master_pipeline.py"


class _Ledger:
    def __init__(self):
        self.records = []

    def record(self, name, payload):
        self.records.append((name, payload))


class _Ingester:
    def __init__(self):
        self.packets = []

    def ingest(self, packet):
        self.packets.append(packet)


class _Storage:
    def __init__(self):
        self.packets = []

    def save(self, packet):
        self.packets.append(packet)


class _Observer:
    def update(self, current_state, control_input, measurement):
        return [current_state[0] + measurement[0]]


class _Controller:
    def compute_control(self, current_state):
        return [current_state[0] * 0.5]


class _Barrier:
    def enforce(self, action):
        return action


class _Acoustics:
    def compute_outlet_noise(self, source_noise_db, duct_length):
        return source_noise_db - duct_length


class _EnergyCost:
    def compute_operational_cost(self, power_kw, duration_hours, tariff_multiplier):
        return power_kw * duration_hours * tariff_multiplier


def _runtime_system():
    return LATCESMasterSystem(
        governance=object(),
        ledger=_Ledger(),
        ingester=_Ingester(),
        observer=_Observer(),
        controller=_Controller(),
        barrier=_Barrier(),
        storage=_Storage(),
    )


def test_master_constructor_has_only_runtime_dependencies():
    parameters = list(inspect.signature(LATCESMasterSystem.__init__).parameters)
    assert parameters == [
        "self",
        "governance",
        "ledger",
        "ingester",
        "observer",
        "controller",
        "barrier",
        "storage",
    ]


def test_master_module_has_no_scientific_model_imports():
    tree = ast.parse(MASTER_PATH.read_text(encoding="utf-8"))
    scientific_imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module and node.module.startswith("lat_ces.scientific"):
            scientific_imports.append(node.module)
        elif isinstance(node, ast.Import):
            scientific_imports.extend(
                alias.name for alias in node.names if alias.name.startswith("lat_ces.scientific")
            )
    assert scientific_imports == []


def test_execute_tick_remains_runtime_only():
    system = _runtime_system()
    packet = SimpleNamespace(sensor_id="S1", quantity=SimpleNamespace(value=2.0))

    result = system.execute_tick(packet, [1.0], [0.1])

    assert result == {
        "sensor_id": "S1",
        "corrected_state": [3.0],
        "safe_action": [0.5],
    }
    assert system.ledger.records == [("MASTER_TICK_STANDARD", result)]
    assert system.ingester.packets == [packet]
    assert system.storage.packets == [packet]


def test_optional_scientific_evaluations_use_explicit_injection():
    system = _runtime_system()

    assert system.evaluate_acoustics_option(_Acoustics(), 50.0, 10.0) == 40.0
    assert system.evaluate_energy_cost_option(_EnergyCost(), 2.5, 4.0, 1.2) == 12.0
    assert system.ledger.records[-1] == (
        "OPTIONAL_COST_EVALUATION",
        {"power_kw": 2.5, "cost": 12.0},
    )
