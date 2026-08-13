"""Controlled mathematical relation for a hardened physical quantity."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Equation:
    expression: str

    def __post_init__(self):
        if not self.expression or not self.expression.strip():
            raise ValueError("Equation cannot be empty")

    def __str__(self) -> str:
        return self.expression
