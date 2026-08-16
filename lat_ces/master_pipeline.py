from typing import Any, Dict

from lat_ces.gov.axiom import ConstitutionalEngine
from lat_ces.gov.provenance import ProvenanceLedger
from lat_ces.twin.telemetry import TelemetryIngester, TelemetryPacket
from lat_ces.twin.observer import LuenbergerObserver
from lat_ces.control.lqr import SimpleLQRController
from lat_ces.control.barrier import SafetyBarrier
from lat_ces.data.timeseries import TimeSeriesStorage


class LATCESMasterSystem:
    """Runtime orchestration core for telemetry, state estimation, control and safety.

    Scientific models are intentionally not constructor dependencies. Scientific
    analyses are injected explicitly into optional evaluation methods so the
    runtime tick remains decoupled from domain-model construction.
    """

    def __init__(
        self,
        governance: ConstitutionalEngine,
        ledger: ProvenanceLedger,
        ingester: TelemetryIngester,
        observer: LuenbergerObserver,
        controller: SimpleLQRController,
        barrier: SafetyBarrier,
        storage: TimeSeriesStorage,
    ):
        self.governance = governance
        self.ledger = ledger
        self.ingester = ingester
        self.observer = observer
        self.controller = controller
        self.barrier = barrier
        self.storage = storage

    def execute_tick(
        self,
        packet: TelemetryPacket,
        current_state: list,
        control_input: list,
        fan_power_kw: float = 0.0,
        mass_flow: float = 0.0,
        delta_temp: float = 0.0,
        relative_humidity: float = 0.0,
        surface_temp: float = 0.0,
        dew_point: float = 0.0,
        operating_hours: float = 0.0,
        inflows: list | None = None,
        outflows: list | None = None,
        current_co2: float = 0.0,
        occupants: int = 0,
        dt_seconds: float = 0.0,
    ) -> Dict[str, Any]:
        # Osnovni, brzi dio tick-a: telemetry, observer, control, safety barrier.
        # Scientific model calculations remain outside this runtime path.
        self.ingester.ingest(packet)
        self.storage.save(packet)
        corrected_state = self.observer.update(current_state, control_input, [packet.quantity.value])
        safe_action = self.barrier.enforce(self.controller.compute_control(current_state))

        tick_metrics = {
            "sensor_id": packet.sensor_id,
            "corrected_state": corrected_state,
            "safe_action": safe_action,
        }
        self.ledger.record("MASTER_TICK_STANDARD", tick_metrics)

        return tick_metrics

    def evaluate_acoustics_option(
        self,
        acoustics_model: Any,
        source_noise_db: float,
        duct_length: float,
    ) -> float:
        """Evaluate acoustic attenuation through an explicitly injected model."""
        return acoustics_model.compute_outlet_noise(source_noise_db, duct_length)

    def evaluate_energy_cost_option(
        self,
        energy_cost_model: Any,
        power_kw: float,
        duration_hours: float,
        tariff_multiplier: float = 1.0,
    ) -> float:
        """Evaluate energy cost through an explicitly injected model."""
        cost = energy_cost_model.compute_operational_cost(power_kw, duration_hours, tariff_multiplier)
        self.ledger.record("OPTIONAL_COST_EVALUATION", {"power_kw": power_kw, "cost": cost})
        return cost
