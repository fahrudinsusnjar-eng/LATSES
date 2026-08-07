"""
LAT-CES Mathematical Core
Differential & Field Engine Reference Implementation (LAT-MATH-CORE-0012)
"""
from typing import Callable
from lat_ces.scientific.units.quantity import Quantity, QuantityError

class FieldError(Exception):
    """Base exception for Differential Field operations."""
    pass

class FieldEngine:
    """
    Executes differential operators over continuous and discrete physical fields.
    Ensures spatial derivative operations correctly update physical units [L^-1].
    """
    @staticmethod
    def gradient_1d(
        field_func: Callable[[Quantity], Quantity], 
        point: Quantity, 
        dx: Quantity
    ) -> Quantity:
        """
        Calculates 1D central finite difference gradient: dF/dx ~ (F(x+dx) - F(x-dx)) / (2*dx)
        """
        if not isinstance(point, Quantity) or not isinstance(dx, Quantity):
            raise FieldError("Point and dx must be Quantity instances.")
        if not point.unit.is_compatible(dx.unit):
            raise FieldError("Spatial increment dx must match point physical dimension.")
            
        f_plus = field_func(point + dx)
        f_minus = field_func(point - dx)
        
        df = f_plus - f_minus
        two_dx = dx * 2.0
        
        return df / two_dx
