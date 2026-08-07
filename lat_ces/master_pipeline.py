from typing import Dict, Any, List
from lat_ces.gov.axiom import ConstitutionalEngine
from lat_ces.gov.provenance import ProvenanceLedger
from lat_ces.twin.telemetry import TelemetryIngester, TelemetryPacket
from lat_ces.twin.observer import LuenbergerObserver
from lat_ces.control.lqr import SimpleLQRController
from lat_ces.control.barrier import SafetyBarrier
from lat_ces.data.timeseries import TimeSeriesStorage
from lat_ces.scientific.plenum import PlenumModel
from lat_ces.scientific.pressure_drop import PressureDropModel
from lat_ces.scientific.energy import EnergyEfficiencyModel
from lat_ces.scientific.thermal import ThermalModel
from lat_ces.scientific.humidity import HumidityModel
from lat_ces.scientific.filter_degradation import FilterModel
from lat_ces.scientific.mass_balance import MassBalanceModel
from lat_ces.scientific.fan_curve import FanCurveModel
from lat_ces.scientific.iaq import IAQModel
from lat_ces.scientific.thermal_comfort import ThermalComfortModel
from lat_ces.scientific.duct_loss import DuctLossModel
from lat_ces.scientific.acoustics import AcousticsModel
from lat_ces.scientific.energy_cost import EnergyCostModel

class LATCESMasterSystem:
    def __init__(
        self,
        governance: ConstitutionalEngine,
        ledger: ProvenanceLedger,
        ingester: TelemetryIngester,
        observer: LuenbergerObserver,
        controller: SimpleLQRController,
        barrier: SafetyBarrier,
        storage: TimeSeriesStorage,
        plenum_model: PlenumModel,
        pressure_model: PressureDropModel,
        energy_model: EnergyEfficiencyModel,
        thermal_model: ThermalModel,
        humidity_model: HumidityModel,
        filter_model: FilterModel,
        mass_balance_model: MassBalanceModel,
        fan_curve_model: FanCurveModel,
        iaq_model: IAQModel,
        thermal_comfort_model: ThermalComfortModel,
        duct_loss_model: DuctLossModel,
        acoustics_model: AcousticsModel,
        energy_cost_model: EnergyCostModel
    ):
        self.governance = governance
        self.ledger = ledger
        self.ingester = ingester
        self.observer = observer
        self.controller = controller
        self.barrier = barrier
        self.storage = storage
        self.plenum_model = plenum_model
        self.pressure_model = pressure_model
        self.energy_model = energy_model
        self.thermal_model = thermal_model
        self.humidity_model = humidity_model
        self.filter_model = filter_model
        self.mass_balance_model = mass_balance_model
        self.fan_curve_model = fan_curve_model
        self.iaq_model = iaq_model
        self.thermal_comfort_model = thermal_comfort_model
        self.duct_loss_model = duct_loss_model
        self.acoustics_model = acoustics_model
        self.energy_cost_model = energy_cost_model

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
        dt_seconds: float = 0.0
    ) -> Dict[str, Any]:
        # Osnovni, brzi dio tik-a (telemetry, observer, control, safety barrier)
        self.ingester.ingest(packet)
        self.storage.save(packet)
        corrected_state = self.observer.update(current_state, control_input, [packet.quantity.value])
        safe_action = self.barrier.enforce(self.controller.compute_control(current_state))

        tick_metrics = {
            "sensor_id": packet.sensor_id,
            "corrected_state": corrected_state,
            "safe_action": safe_action
        }
        self.ledger.record("MASTER_TICK_STANDARD", tick_metrics)

        return tick_metrics

    def evaluate_acoustics_option(self, source_noise_db: float, duct_length: float) -> float:
        """Opcija 1: Izračun akustičke atenuacije na zahtjev."""
        return self.acoustics_model.compute_outlet_noise(source_noise_db, duct_length)

    def evaluate_energy_cost_option(self, power_kw: float, duration_hours: float, tariff_multiplier: float = 1.0) -> float:
        """Opcija 2: Izračun finansijskog troška energije na zahtjev."""
        cost = self.energy_cost_model.compute_operational_cost(power_kw, duration_hours, tariff_multiplier)
        self.ledger.record("OPTIONAL_COST_EVALUATION", {"power_kw": power_kw, "cost": cost})
        return cost
