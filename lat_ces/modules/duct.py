"""
LAT-CES Module 016: Duct Friction & Friction Loss Engine
Dokument: LAT-SCI-MOD-0016
"""
import math
from lat_ces.core.dimensions import Dimension, DENSITY, VELOCITY, LENGTH
from lat_ces.modules.quantity import PhysicalQuantity
from lat_ces.modules.pressure import PRESSURE

# Dinamička viskoznost zraka na sobnoj temperaturi (Pa·s -> kg/(m·s))
VISCOSITY_AIR = Dimension(M=1, L=-1, T=-1)

class DuctFrictionEngine:
    @staticmethod
    def calculate_reynolds_number(
        density: PhysicalQuantity,
        velocity: PhysicalQuantity,
        hydraulic_diameter: PhysicalQuantity,
        dynamic_viscosity: PhysicalQuantity
    ) -> float:
        """
        Računa bezdimenzionalni Reynoldsov broj (Re).
        """
        re = (density.value * velocity.value * hydraulic_diameter.value) / dynamic_viscosity.value
        return re

    @staticmethod
    def estimate_friction_factor(reynolds: float) -> float:
        """
        Određuje Darcy-Weisbachov faktor trenja (f).
        Laminarno (Re < 2300): f = 64 / Re
        Turbulentno (Re >= 2300): Aproksimacija za glatke kanale f = 0.3164 / Re^0.25 (Blasius)
        """
        if reynolds <= 0:
            raise ValueError("Reynoldsov broj mora biti pozitivan!")
        if reynolds < 2300.0:
            return 64.0 / reynolds
        else:
            return 0.3164 / (reynolds ** 0.25)

    def calculate_friction_loss(
        self,
        friction_factor: float,
        length: PhysicalQuantity,
        hydraulic_diameter: PhysicalQuantity,
        density: PhysicalQuantity,
        velocity: PhysicalQuantity
    ) -> PhysicalQuantity:
        """
        Računa pad pritiska uslijed trenja u kanalu:
        delta_P = f * (L / D_h) * (rho * v^2 / 2)
        """
        dp_value = friction_factor * (length.value / hydraulic_diameter.value) * (density.value * (velocity.value ** 2) / 2.0)

        u_rel = math.sqrt(
            (length.uncertainty / length.value)**2 +
            (hydraulic_diameter.uncertainty / hydraulic_diameter.value)**2 +
            (density.uncertainty / density.value)**2 +
            (2.0 * velocity.uncertainty / velocity.value)**2
        )

        return PhysicalQuantity(
            value=dp_value,
            dimension=PRESSURE,
            uncertainty=dp_value * u_rel
        )