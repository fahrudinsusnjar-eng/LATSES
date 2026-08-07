import os
import subprocess

files = {
    "lat_ces/modules/fittings.py": '''"""
LAT-CES Module 017: Fitting Loss Engine
Dokument: LAT-SCI-MOD-0017
"""
import math
from lat_ces.core.dimensions import DENSITY, VELOCITY
from lat_ces.modules.quantity import PhysicalQuantity
from lat_ces.modules.pressure import PRESSURE

class FittingLossEngine:
    @staticmethod
    def calculate_fitting_loss(
        zeta: float,
        density: PhysicalQuantity,
        velocity: PhysicalQuantity
    ) -> PhysicalQuantity:
        """
        Računa lokalni pad pritiska na fitingu: delta_P = zeta * (rho * v^2 / 2)
        """
        if zeta < 0:
            raise ValueError("Koeficijent otpora (zeta) ne može biti negativan!")

        dp_val = zeta * (density.value * (velocity.value ** 2) / 2.0)

        u_rel = math.sqrt(
            (density.uncertainty / density.value)**2 +
            (2.0 * velocity.uncertainty / velocity.value)**2
        )

        return PhysicalQuantity(
            value=dp_val,
            dimension=PRESSURE,
            uncertainty=dp_val * u_rel
        )
''',
    "tests/test_fittings.py": '''import math
from lat_ces.core.dimensions import DENSITY, VELOCITY
from lat_ces.modules.quantity import PhysicalQuantity
from lat_ces.modules.pressure import PRESSURE
from lat_ces.modules.fittings import FittingLossEngine


def test_fitting_loss():
    engine = FittingLossEngine()

    zeta = 0.5
    rho = PhysicalQuantity(1.2, DENSITY, 0.01)
    v = PhysicalQuantity(4.0, VELOCITY, 0.1)

    dp = engine.calculate_fitting_loss(zeta, rho, v)

    assert math.isclose(dp.value, 4.8, abs_tol=1e-2)
    assert dp.dimension == PRESSURE
    assert dp.uncertainty > 0
''',
    "lat_ces/modules/fan_laws.py": '''"""
LAT-CES Module 018: Fan Affinity Laws Engine
Dokument: LAT-SCI-MOD-0018
"""
from lat_ces.modules.quantity import PhysicalQuantity
from lat_ces.modules.plenum import FLOW_RATE
from lat_ces.modules.pressure import PRESSURE, POWER

class FanAffinityEngine:
    @staticmethod
    def scale_by_rpm(
        flow: PhysicalQuantity,
        pressure: PhysicalQuantity,
        power: PhysicalQuantity,
        n1_rpm: float,
        n2_rpm: float
    ):
        """
        Preračunava parametre ventilatora pri promjeni obrtaja sa n1 na n2:
        Q2 = Q1 * (n2/n1)
        P2 = P1 * (n2/n1)^2
        W2 = W1 * (n2/n1)^3
        """
        if n1_rpm <= 0 or n2_rpm <= 0:
            raise ValueError("Broj obrtaja (RPM) mora biti pozitivan!")

        ratio = n2_rpm / n1_rpm

        scaled_q = PhysicalQuantity(flow.value * ratio, FLOW_RATE, flow.uncertainty * ratio)
        scaled_p = PhysicalQuantity(pressure.value * (ratio**2), PRESSURE, pressure.uncertainty * (ratio**2))
        scaled_w = PhysicalQuantity(power.value * (ratio**3), POWER, power.uncertainty * (ratio**3))

        return scaled_q, scaled_p, scaled_w
''',
    "tests/test_fan_laws.py": '''import math
from lat_ces.modules.quantity import PhysicalQuantity
from lat_ces.modules.plenum import FLOW_RATE
from lat_ces.modules.pressure import PRESSURE, POWER
from lat_ces.modules.fan_laws import FanAffinityEngine


def test_fan_laws_scaling():
    engine = FanAffinityEngine()

    q1 = PhysicalQuantity(2.0, FLOW_RATE, 0.05)
    p1 = PhysicalQuantity(200.0, PRESSURE, 10.0)
    w1 = PhysicalQuantity(500.0, POWER, 25.0)

    q2, p2, w2 = engine.scale_by_rpm(q1, p1, w1, 1000.0, 2000.0)

    assert q2.value == 4.0
    assert p2.value == 800.0
    assert w2.value == 4000.0
''',
    "lat_ces/modules/psychrometrics.py": '''"""
LAT-CES Module 019: Psychrometrics & Humidity Engine
Dokument: LAT-SCI-MOD-0019
"""
import math

class PsychrometricEngine:
    @staticmethod
    def saturation_vapor_pressure_pa(temp_celsius: float) -> float:
        """Pritisak zasićenja vodene pare u Paskalima (Magnusova formula)."""
        return 610.78 * math.exp((17.27 * temp_celsius) / (temp_celsius + 237.3))

    @staticmethod
    def calculate_relative_humidity(actual_vapor_pressure_pa: float, temp_celsius: float) -> float:
        """Računa relativnu vlažnost zraka RH (%) = (p_v / p_sat) * 100."""
        p_sat = PsychrometricEngine.saturation_vapor_pressure_pa(temp_celsius)
        if p_sat <= 0:
            return 0.0
        rh = (actual_vapor_pressure_pa / p_sat) * 100.0
        return min(max(rh, 0.0), 100.0)
''',
    "tests/test_psychrometrics.py": '''import math
from lat_ces.modules.psychrometrics import PsychrometricEngine


def test_psychrometrics():
    engine = PsychrometricEngine()

    p_sat = engine.saturation_vapor_pressure_pa(20.0)
    assert math.isclose(p_sat, 2338.0, abs_tol=50.0)

    rh_100 = engine.calculate_relative_humidity(p_sat, 20.0)
    assert math.isclose(rh_100, 100.0, abs_tol=1e-2)
''',
    "lat_ces/modules/pipeline_v3.py": '''"""
LAT-CES Module 020: Full Duct Network Integration Simulator v3
Spaja Module 010 do 019 u celovitu mrežnu simulaciju kanala.
"""
from typing import Dict, Any
from lat_ces.core.dimensions import VELOCITY, LENGTH, DENSITY
from lat_ces.modules.quantity import PhysicalQuantity
from lat_ces.modules.plenum import PlenumEngine, AREA
from lat_ces.modules.duct import DuctFrictionEngine, VISCOSITY_AIR
from lat_ces.modules.fittings import FittingLossEngine
from lat_ces.modules.pressure import FanEngine, PRESSURE
from lat_ces.modules.psychrometrics import PsychrometricEngine

class DuctNetworkSimulation:
    def __init__(self, max_allowed_pressure_pa: float = 500.0):
        self.plenum_engine = PlenumEngine()
        self.duct_engine = DuctFrictionEngine()
        self.fitting_engine = FittingLossEngine()
        self.fan_engine = FanEngine()
        self.psych_engine = PsychrometricEngine()
        self.max_allowed_pressure_pa = max_allowed_pressure_pa

    def run_network_simulation(
        self,
        area: PhysicalQuantity,
        velocity: PhysicalQuantity,
        density: PhysicalQuantity,
        duct_length: PhysicalQuantity,
        hydraulic_diameter: PhysicalQuantity,
        fitting_zeta_sum: float,
        temp_celsius: float,
        vapor_pressure_pa: float
    ) -> Dict[str, Any]:
        """Izvršava cjelovitu analizu mreže kanala."""
        airflow = self.plenum_engine.calculate_airflow(area, velocity)

        mu = PhysicalQuantity(1.81e-5, VISCOSITY_AIR, 1e-7)
        re = self.duct_engine.calculate_reynolds_number(density, velocity, hydraulic_diameter, mu)
        f = self.duct_engine.estimate_friction_factor(re)
        dp_friction = self.duct_engine.calculate_friction_loss(f, duct_length, hydraulic_diameter, density, velocity)

        dp_fittings = self.fitting_engine.calculate_fitting_loss(fitting_zeta_sum, density, velocity)

        total_dp_val = dp_friction.value + dp_fittings.value
        total_dp = PhysicalQuantity(total_dp_val, PRESSURE, dp_friction.uncertainty + dp_fittings.uncertainty)

        fan_power = self.fan_engine.calculate_fan_power(airflow, total_dp, efficiency=0.8)

        rh = self.psych_engine.calculate_relative_humidity(vapor_pressure_pa, temp_celsius)

        status = "PASS" if total_dp.value <= self.max_allowed_pressure_pa else "FAIL"

        return {
            "airflow": airflow,
            "reynolds": re,
            "dp_friction": dp_friction,
            "dp_fittings": dp_fittings,
            "total_dp": total_dp,
            "fan_power": fan_power,
            "relative_humidity": rh,
            "status": status
        }
''',
    "tests/test_pipeline_v3.py": '''import math
from lat_ces.core.dimensions import VELOCITY, LENGTH, DENSITY
from lat_ces.modules.quantity import PhysicalQuantity
from lat_ces.modules.plenum import AREA
from lat_ces.modules.pipeline_v3 import DuctNetworkSimulation


def test_full_network_simulation():
    sim = DuctNetworkSimulation(max_allowed_pressure_pa=500.0)

    area = PhysicalQuantity(1.0, AREA, 0.02)
    velocity = PhysicalQuantity(3.0, VELOCITY, 0.1)
    density = PhysicalQuantity(1.2, DENSITY, 0.01)
    duct_length = PhysicalQuantity(20.0, LENGTH, 0.2)
    d_h = PhysicalQuantity(0.5, LENGTH, 0.01)
    fitting_zeta_sum = 1.5
    temp_c = 22.0
    v_press = 1200.0

    report = sim.run_network_simulation(
        area, velocity, density, duct_length, d_h, fitting_zeta_sum, temp_c, v_press
    )

    assert report["airflow"].value == 3.0
    assert report["reynolds"] > 2300.0
    assert report["total_dp"].value > 0
    assert report["fan_power"].value > 0
    assert 0.0 <= report["relative_humidity"] <= 100.0
    assert report["status"] == "PASS"
'''
}

print("🚀 Kreiram fajlove za BLOK 3 (Moduli 017, 018, 019 i 020)...")
for filepath, content in files.items():
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"  [OK] Kreiran: {filepath}")

print("\n🧪 Pokrećem pytest verifikaciju kompletnog repozitorija...")
test_res = subprocess.run(["pytest"], capture_output=True, text=True)

if test_res.returncode == 0:
    print("✅ Svi testovi su PROŠLI! Šaljem BLOK 3 na GitHub...")
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", "feat(block-3): Implementirani Moduli 017-020 sa Mreznim Integracijskim Simulatorom"])
    subprocess.run(["git", "tag", "-a", "v1.0.0-block3", "-m", "LAT-CES Blok 3 (Moduli 017-020) dovrsen"])
    subprocess.run(["git", "push", "origin", "main"])
    subprocess.run(["git", "push", "origin", "v1.0.0-block3"])
    print("\n🎉 BLOK 3 je uspješno verifikovan i zamrznut pod tagom v1.0.0-block3!")
else:
    print("❌ Testovi nisu prošli! Pogledajte grešku:")
    print(test_res.stdout)
    print(test_res.stderr)
