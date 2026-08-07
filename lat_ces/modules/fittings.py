"""
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