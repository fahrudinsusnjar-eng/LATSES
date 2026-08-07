"""
LAT-CES Core: Dimension Engine (SI Base Units Algebra)
Dokumenti: LAT-SCI-CORE-0006 do LAT-SCI-CORE-0009
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Dimension:
    """Seven-base SI dimensional algebra with multiplication and division."""

    L: int = 0
    M: int = 0
    T: int = 0
    I: int = 0
    Theta: int = 0
    N: int = 0
    J: int = 0

    def __mul__(self, other: "Dimension") -> "Dimension":
        return Dimension(
            L=self.L + other.L,
            M=self.M + other.M,
            T=self.T + other.T,
            I=self.I + other.I,
            Theta=self.Theta + other.Theta,
            N=self.N + other.N,
            J=self.J + other.J,
        )

    def __truediv__(self, other: "Dimension") -> "Dimension":
        return Dimension(
            L=self.L - other.L,
            M=self.M - other.M,
            T=self.T - other.T,
            I=self.I - other.I,
            Theta=self.Theta - other.Theta,
            N=self.N - other.N,
            J=self.J - other.J,
        )

    def is_dimensionless(self) -> bool:
        return all(
            value == 0
            for value in [self.L, self.M, self.T, self.I, self.Theta, self.N, self.J]
        )


DIMENSIONLESS = Dimension()
LENGTH = Dimension(L=1)
MASS = Dimension(M=1)
TIME = Dimension(T=1)
VELOCITY = Dimension(L=1, T=-1)
DENSITY = Dimension(M=1, L=-3)
ACCELERATION = Dimension(L=1, T=-2)
FORCE = Dimension(M=1, L=1, T=-2)
