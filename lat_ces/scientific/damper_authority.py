class DamperError(Exception):
    pass


class DamperAuthorityModel:
    def __init__(self):
        pass

    def compute_authority(self, dp_damper_fully_open: float, dp_system_total: float) -> float:
        r"""
        Izračunava autoritet klapne (vrijednost od 0 do 1).
        Formula: Authority = dP_damper_fully_open / dP_system_total
        Preporučeno je da autoritet bude > 0.1 za stabilnu kontrolu.
        """
        if dp_damper_fully_open < 0.0 or dp_system_total <= 0.0:
            raise DamperError("Pressure drops must be valid and total system drop must be > 0.")
        if dp_damper_fully_open > dp_system_total:
            raise DamperError("Damper pressure drop cannot exceed total system pressure drop.")

        authority = dp_damper_fully_open / dp_system_total
        return round(authority, 4)
