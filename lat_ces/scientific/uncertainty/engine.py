"""
LAT-CES Scientific Core
Uncertainty & Error Analysis Engine Reference Implementation (LAT-SCI-CORE-0021)
"""

import math

from lat_ces.scientific.units.quantity import Quantity, QuantityError


class UncertaintyEngine:
    """
    Executes analytical error propagation according to GUM guidelines.
    """

    @staticmethod
    def add(q1: Quantity, q2: Quantity) -> Quantity:
        """Propagates uncertainty for addition: u_c = sqrt(u1^2 + u2^2)"""
        return q1 + q2  # Implemented under the hood in Quantity engine

    @staticmethod
    def subtract(q1: Quantity, q2: Quantity) -> Quantity:
        """Propagates uncertainty for subtraction: u_c = sqrt(u1^2 + u2^2)"""
        return q1 - q2

    @staticmethod
    def multiply(q1: Quantity, q2: Quantity) -> Quantity:
        """Propagates uncertainty for multiplication using relative uncertainty quadrature."""
        return q1 * q2

    @staticmethod
    def divide(q1: Quantity, q2: Quantity) -> Quantity:
        """Propagates uncertainty for division using relative uncertainty quadrature."""
        return q1 / q2

    @staticmethod
    def power(q: Quantity, exponent: float) -> Quantity:
        """
        Propagates uncertainty for power operations: y = x^n
        u(y) = |n * x^(n-1)| * u(x)
        """
        if not isinstance(q, Quantity):
            raise QuantityError("Power operation requires a valid Quantity.")

        new_value = q.value ** exponent
        new_unit = q.unit ** exponent if hasattr(q.unit, "__pow__") else q.unit

        if q.value == 0:
            new_uncertainty = 0.0
        else:
            rel_unc = abs(exponent) * (q.uncertainty / abs(q.value))
            new_uncertainty = abs(new_value) * rel_unc

        return Quantity(value=new_value, unit=new_unit, uncertainty=new_uncertainty)
