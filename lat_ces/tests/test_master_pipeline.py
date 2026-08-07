"""
LAT-CES Master Integration Tests
End-to-End Execution Pipeline Verification
"""

import pytest
from datetime import datetime, timezone

from lat_ces.scientific.units.unit import METER
from lat_ces.scientific.units.quantity import Quantity
from lat_ces.gov.axiom import ConstitutionalEngine
from lat_ces.gov.provenance import ProvenanceLedger
from lat_ces.twin.telemetry import TelemetryIngester, TelemetryPacket
from lat_ces.twin.observer import LuenbergerObserver
from lat_ces.control.lqr import SimpleLQRController
from lat_ces.control.barrier import SafetyBarrier
from lat_ces.data.timeseries import TimeSeriesStorage
from lat_ces.master_pipeline import LATCESMasterSystem
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


def test_master_pipeline_full_lifecycle():
    # 1. Inicijalizacija svih temeljnih motora ekosistema
    governance = ConstitutionalEngine()
    governance.add_axiom("VAL_LIMIT", lambda state: state.get("value", 0) < 100.0)

    ledger = ProvenanceLedger(file_path="data/test_master_pipeline_ledger.jsonl")
    ledger.clear_history()
    ingester = TelemetryIngester()
    storage = TimeSeriesStorage()

    # Matrice sistema (1 stanje, 1 ulaz, 1 izlaz)
    A = [[-1.0]]
    B = [[1.0]]
    C = [[1.0]]
    L = [[0.5]]  # Observer gain
    observer = LuenbergerObserver(A=A, B=B, C=C, L=L)

    # LQR Kontroler: u = -K * x -> K = [[2.0]]
    K = [[2.0]]
    controller = SimpleLQRController(K_gain=K)

    # Ustavne sigurnosne barijere
    barrier = SafetyBarrier(min_limit=-10.0, max_limit=10.0)

    # Scientific modeli
    plenum_model = PlenumModel(cross_section_area=2.0)
    pressure_model = PressureDropModel(loss_coefficient=1.2)
    energy_model = EnergyEfficiencyModel()
    thermal_model = ThermalModel()
    humidity_model = HumidityModel()
    filter_model = FilterModel(base_resistance=100.0, degradation_rate=0.01)
    mass_balance_model = MassBalanceModel()
    fan_curve_model = FanCurveModel(max_pressure=500.0, coefficient_a=200.0)
    iaq_model = IAQModel(room_volume_m3=100.0)
    thermal_comfort_model = ThermalComfortModel()
    duct_loss_model = DuctLossModel(surface_area=10.0, overall_heat_transfer_coef=1.2)
    acoustics_model = AcousticsModel(duct_attenuation_rate=0.5, silencer_insertion_loss=10.0)
    energy_cost_model = EnergyCostModel(base_tariff_per_kwh=0.15)

    # Sastavljanje Master Sistema
    master_system = LATCESMasterSystem(
        governance=governance,
        ledger=ledger,
        ingester=ingester,
        observer=observer,
        controller=controller,
        barrier=barrier,
        storage=storage,
        plenum_model=plenum_model,
        pressure_model=pressure_model,
        energy_model=energy_model,
        thermal_model=thermal_model,
        humidity_model=humidity_model,
        filter_model=filter_model,
        mass_balance_model=mass_balance_model,
        fan_curve_model=fan_curve_model,
        iaq_model=iaq_model,
        thermal_comfort_model=thermal_comfort_model,
        duct_loss_model=duct_loss_model,
        acoustics_model=acoustics_model,
        energy_cost_model=energy_cost_model,
    )

    # 2. Priprema telemetrijskog paketa
    q = Quantity(25.0, METER, uncertainty=0.1)
    packet = TelemetryPacket(
        sensor_id="SENSOR-PLENUM-01",
        quantity=q,
        timestamp=datetime.now(timezone.utc),
    )

    current_state = [10.0]
    control_input = [1.0]

    # 3. Izvršavanje Master Ciklusa (Tick)
    tick_metrics = master_system.execute_tick(
        packet=packet,
        current_state=current_state,
        control_input=control_input,
        fan_power_kw=5.0,
        mass_flow=1.2,
        delta_temp=8.0,
        relative_humidity=70.0,
        surface_temp=18.0,
        dew_point=12.0,
        operating_hours=100.0,
        inflows=[1.2, 0.8],
        outflows=[1.0, 0.9, 0.1],
        current_co2=600.0,
        occupants=3,
        dt_seconds=60.0,
    )

    # 4. Verifikacija rezultata integracije
    # Provjera unosa i perzistencije telemetrije
    latest_packet = ingester.get_latest("SENSOR-PLENUM-01")
    assert latest_packet.quantity.value == 25.0

    stored_packets = storage.query("SENSOR-PLENUM-01", packet.timestamp, packet.timestamp)
    assert len(stored_packets) == 1

    # Provjera ustavnog revizorskog traga (Ledger)
    history = ledger.get_history()
    assert len(history) == 1
    assert history[0]["event"] == "MASTER_TICK_STANDARD"
    assert history[0]["metrics"]["sensor_id"] == "SENSOR-PLENUM-01"

    # Provjera generisane i filtrirane upravljačke akcije
    assert isinstance(tick_metrics, dict)
    assert isinstance(tick_metrics["safe_action"], list)
    assert len(tick_metrics["safe_action"]) == 1
    assert "corrected_state" in tick_metrics


def test_optional_cost_evaluation():
    governance = ConstitutionalEngine()
    ledger = ProvenanceLedger(file_path="data/test_master_pipeline_ledger.jsonl")
    ledger.clear_history()
    ingester = TelemetryIngester()
    storage = TimeSeriesStorage()
    observer = LuenbergerObserver(A=[[-1.0]], B=[[1.0]], C=[[1.0]], L=[[0.5]])
    controller = SimpleLQRController(K_gain=[[2.0]])
    barrier = SafetyBarrier(min_limit=-10.0, max_limit=10.0)

    master_system = LATCESMasterSystem(
        governance=governance,
        ledger=ledger,
        ingester=ingester,
        observer=observer,
        controller=controller,
        barrier=barrier,
        storage=storage,
        plenum_model=PlenumModel(cross_section_area=2.0),
        pressure_model=PressureDropModel(loss_coefficient=1.2),
        energy_model=EnergyEfficiencyModel(),
        thermal_model=ThermalModel(),
        humidity_model=HumidityModel(),
        filter_model=FilterModel(base_resistance=100.0, degradation_rate=0.01),
        mass_balance_model=MassBalanceModel(),
        fan_curve_model=FanCurveModel(max_pressure=500.0, coefficient_a=200.0),
        iaq_model=IAQModel(room_volume_m3=100.0),
        thermal_comfort_model=ThermalComfortModel(),
        duct_loss_model=DuctLossModel(surface_area=10.0, overall_heat_transfer_coef=1.2),
        acoustics_model=AcousticsModel(duct_attenuation_rate=0.5, silencer_insertion_loss=10.0),
        energy_cost_model=EnergyCostModel(base_tariff_per_kwh=0.15),
    )

    cost = master_system.evaluate_energy_cost_option(power_kw=2.5, duration_hours=2.0)
    assert cost > 0.0

    history = ledger.get_history()
    assert history[-1]["event"] == "OPTIONAL_COST_EVALUATION"
    ledger.clear_history()

    ledger.clear_history()
