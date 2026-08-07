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
from lat_ces.master_pipeline import LATCESMasterSystem

def main():
    print("=== Pokretanje LAT-CES Master Sistema (Moduli 23-27 Integrisani) ===")
    
    governance = ConstitutionalEngine()
    CRITICAL_FILTER_LIMIT = 13.0
    governance.add_axiom(
        "MAX_FILTER_RESISTANCE_AXIOM",
        lambda state: state.get("filter_resistance", 0.0) <= CRITICAL_FILTER_LIMIT
    )
    
    ledger = ProvenanceLedger()
    ingester = TelemetryIngester()
    storage = TimeSeriesStorage()
    
    plenum_model = PlenumModel(cross_section_area=0.25)
    pressure_model = PressureDropModel(loss_coefficient=1.5, air_density=1.2)
    energy_model = EnergyEfficiencyModel()
    thermal_model = ThermalModel(specific_heat_capacity=1005.0)
    humidity_model = HumidityModel()
    filter_model = FilterModel(base_resistance=100.0, degradation_rate=0.01)
    mass_balance_model = MassBalanceModel()
    fan_curve_model = FanCurveModel(max_pressure=500.0, coefficient_a=200.0)
    iaq_model = IAQModel(room_volume_m3=100.0)
    thermal_comfort_model = ThermalComfortModel()
    duct_loss_model = DuctLossModel(surface_area=10.0, overall_heat_transfer_coef=1.2)
    acoustics_model = AcousticsModel(duct_attenuation_rate=0.5, silencer_insertion_loss=10.0)
    energy_cost_model = EnergyCostModel(base_tariff_per_kwh=0.15)

    A = [[-1.2]]
    B = [[1.0]]
    C = [[1.0]]
    L = [[0.4]]
    observer = LuenbergerObserver(A=A, B=B, C=C, L=L)

    K = [[1.5]]
    controller = SimpleLQRController(K_gain=K)
    barrier = SafetyBarrier(min_limit=-15.0, max_limit=15.0)
    
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
        energy_cost_model=energy_cost_model
    )
    
    current_state = [2.0]
    control_input = [0.1]
    
    print("\n--- Izvršavanje ciklusa sa termalnom i vlažnosnom analizom ---")
    for i in range(1, 4):
        flow_rate = 0.4 + (i * 0.1)
        q = Quantity(flow_rate, METER, uncertainty=0.01)
        packet = TelemetryPacket(
            sensor_id="SENSOR-PLENUM-COMPREHENSIVE",
            quantity=q,
            timestamp=datetime.now(timezone.utc)
        )

        metrics = master_system.execute_tick(
            packet=packet,
            current_state=current_state,
            control_input=control_input,
            fan_power_kw=1.2,
            mass_flow=0.5 + (i * 0.1),
            delta_temp=12.0,
            relative_humidity=82.0 + (i * 4.0),
            surface_temp=14.0,
            dew_point=15.5,
            operating_hours=100.0 + i,
            inflows=[1.2, 0.8],
            outflows=[1.0, 0.9, 0.1],
            current_co2=600.0,
            occupants=3,
            dt_seconds=60.0
        )
        print(f"Tick {i} -> Corrected state: {metrics['corrected_state']} | Safe action: {metrics['safe_action']}")

    # Kada zatreba finansijska analiza (opcija)
    current_cost = master_system.evaluate_energy_cost_option(power_kw=2.5, duration_hours=4.0)
    print(f"Trenutni trošak rada: {current_cost} BAM")

    print(f"\n[USPJESNO] Završeno. Ukupno zapisa: {len(ledger.get_history())}")

    # Poziv izvještaja
    from reports.generate_filter_report import generate_filter_report
    generate_filter_report()

if __name__ == "__main__":
    main()
