class MassBalanceError(Exception):
    pass


class MassBalanceModel:
    def verify_conservation(self, inflows: list, outflows: list, tolerance: float = 1e-2) -> bool:
        """Verifies if total mass inflow matches total mass outflow within tolerance."""
        total_in = sum(inflows)
        total_out = sum(outflows)
        if total_in < 0.0 or total_out < 0.0:
            raise MassBalanceError("Mass flows cannot be negative.")
        return abs(total_in - total_out) <= tolerance
