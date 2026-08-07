class AxiomViolationError(Exception):
    """Izuzetak koji se baca u slučaju kršenja ustavnih aksioma sistema."""
    pass


class ConstitutionalEngine:
    def __init__(self):
        self.axioms = {}

    def add_axiom(self, name: str, rule_func):
        """Dodaje pravilo (aksiom) u sistem."""
        self.axioms[name] = rule_func

    def verify_state(self, state_payload: dict) -> list:
        """
        Provjerava stanje sistema prema svim definisanim aksiomima.
        Vraća listu prekršenih aksioma.
        """
        violations = []
        for name, rule in self.axioms.items():
            try:
                if not rule(state_payload):
                    violations.append(name)
            except Exception as e:
                violations.append(f"{name}_ERROR_{str(e)}")
        return violations
