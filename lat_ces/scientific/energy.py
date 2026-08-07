class EnergyError(Exception):
    pass


class EnergyEfficiencyModel:
    def compute_specific_fan_power(self, fan_power_kw: float, airflow_m3s: float) -> float:
        """Computes Specific Fan Power (SFP) in kW/(m^3/s)."""
        if fan_power_kw < 0.0:
            raise EnergyError("Fan power cannot be negative.")
        if airflow_m3s <= 0.0:
            raise EnergyError("Airflow must be strictly positive.")

        sfp = fan_power_kw / airflow_m3s
        return round(sfp, 3)

    def evaluate_efficiency_class(self, sfp: float) -> str:
        """Categorizes SFP into standard energy efficiency grades."""
        if sfp <= 1.5:
            return "SFP 1 (High Efficiency)"
        elif sfp <= 2.5:
            return "SFP 2 (Standard Efficiency)"
        else:
            return "SFP 3 (Low Efficiency / High Consumption)"
