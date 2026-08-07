class ChillerError(Exception):
    pass


class ChillerModel:
    def __init__(self, nominal_cop: float):
        if nominal_cop <= 0.0:
            raise ChillerError("Nominal COP must be positive.")
        self.nominal_cop = nominal_cop

    def compute_actual_cop(self, plr: float) -> float:
        r"""
        Izračunava stvarni COP chillera na osnovu odnosa opterećenja (PLR).
        PLR (Part Load Ratio) je u rasponu od 0.0 do 1.0 (ili više ako je preopterećen).
        """
        if plr < 0.0:
            raise ChillerError("PLR cannot be negative.")

        # Pojednostavljena inženjerska kriva efikasnosti pri djelimičnom opterećenju
        # COP obično raste pri manjim opterećenjima do neke tačke, pa opada.
        # Aproksimacija: korigujemo nominalni COP preko polinomne zavisnosti od PLR-a.
        efficiency_modifier = 1.0 + 0.3 * plr - 0.2 * (plr ** 2)
        actual_cop = self.nominal_cop * efficiency_modifier

        return round(max(actual_cop, 0.5), 2)
