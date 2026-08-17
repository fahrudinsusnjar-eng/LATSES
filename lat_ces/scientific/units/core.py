from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4

@dataclass(frozen=True)
class Dimension:
    L: int = 0
    M: int = 0
    T: int = 0
    I: int = 0
    Theta: int = 0
    N: int = 0
    J: int = 0

    def __mul__(self, other: "Dimension") -> "Dimension":
        return Dimension(L=self.L + other.L, M=self.M + other.M, T=self.T + other.T, I=self.I + other.I, Theta=self.Theta + other.Theta, N=self.N + other.N, J=self.J + other.J)
    def __truediv__(self, other: "Dimension") -> "Dimension":
        return Dimension(L=self.L - other.L, M=self.M - other.M, T=self.T - other.T, I=self.I - other.I, Theta=self.Theta - other.Theta, N=self.N - other.N, J=self.J - other.J)
    def __pow__(self, power: int | float) -> "Dimension":
        return Dimension(L=self.L * int(power), M=self.M * int(power), T=self.T * int(power), I=self.I * int(power), Theta=self.Theta * int(power), N=self.N * int(power), J=self.J * int(power))
    def is_dimensionless(self) -> bool:
        return all(value == 0 for value in (self.L, self.M, self.T, self.I, self.Theta, self.N, self.J))

class UnitSKOError(ValueError):
    pass

class Unit:
    VALID_STATUSES = {"DRAFT", "REVIEWED", "VERIFIED", "VALIDATED", "RELEASED"}
    def __init__(self, name, symbol, dimension, scale_factor=1.0, offset=0.0, unit_uuid=None, status="DRAFT"):
        if status not in self.VALID_STATUSES:
            raise UnitSKOError(f"Nevažeći status: {status}. Dozvoljeni statusi: {self.VALID_STATUSES}")
        self._name, self._symbol, self._dimension = name, symbol, dimension
        self._scale_factor, self._offset = float(scale_factor), float(offset)
        self._uuid, self._status = unit_uuid or str(uuid4()), status
    @property
    def name(self): return self._name
    @property
    def symbol(self): return self._symbol
    @property
    def dimension(self): return self._dimension
    @property
    def scale_factor(self): return self._scale_factor
    @property
    def offset(self): return self._offset
    @property
    def uuid(self): return self._uuid
    @property
    def status(self): return self._status
    def set_status(self, new_status):
        if self._status == "RELEASED": raise UnitSKOError("Jedinica u stanju RELEASED je nepromjenjiva i ne može mijenjati status.")
        if new_status not in self.VALID_STATUSES: raise UnitSKOError(f"Nevažeći target status: {new_status}")
        self._status = new_status
    def _check_affine_safety(self):
        if self._offset != 0.0: raise UnitSKOError(f"Jedinica '{self.symbol}' ima temperaturni pomak i ne može učestvovati u algebri složenih jedinica bez prethodne konverzije.")
    def __mul__(self, other):
        self._check_affine_safety()
        if isinstance(other, Unit):
            other._check_affine_safety(); return Unit(f"({self.name} * {other.name})", f"{self.symbol}·{other.symbol}", self.dimension * other.dimension, self.scale_factor * other.scale_factor, status="DRAFT")
        if isinstance(other, (int, float)): return Unit(f"Scaled({self.name})", self.symbol, self.dimension, self.scale_factor * float(other), offset=self.offset, status="DRAFT")
        return NotImplemented
    def __rmul__(self, other): return self.__mul__(other)
    def __truediv__(self, other):
        self._check_affine_safety()
        if isinstance(other, Unit):
            other._check_affine_safety(); return Unit(f"({self.name} / {other.name})", f"{self.symbol}/{other.symbol}", self.dimension / other.dimension, self.scale_factor / other.scale_factor, status="DRAFT")
        if isinstance(other, (int, float)): return Unit(f"Scaled({self.name})", self.symbol, self.dimension, self.scale_factor / float(other), offset=self.offset, status="DRAFT")
        return NotImplemented
    def __pow__(self, power):
        self._check_affine_safety(); return Unit(f"({self.name}^{power})", f"{self.symbol}^{power}", self.dimension ** power, float(self.scale_factor ** power), status="DRAFT")
    def __eq__(self, other):
        if not isinstance(other, Unit): return NotImplemented
        return self.symbol == other.symbol and self.dimension == other.dimension and self.scale_factor == other.scale_factor and self.offset == other.offset
    def __setattr__(self, name, value):
        if name in {"_status", "_name", "_symbol", "_dimension", "_scale_factor", "_offset", "_uuid"} and getattr(self, "_status", None) == "RELEASED": raise UnitSKOError("Jedinica u stanju RELEASED je nepromjenjiva i ne može mijenjati parametre.")
        super().__setattr__(name, value)
    def __repr__(self): return f"Unit(symbol='{self.symbol}', status='{self.status}', uuid='{self.uuid[:8]}...')"

SIUnit = Unit
DIMENSIONLESS = Dimension(); LENGTH = Dimension(L=1); MASS = Dimension(M=1); TIME = Dimension(T=1); CURRENT = Dimension(I=1); TEMPERATURE = Dimension(Theta=1); AMOUNT = Dimension(N=1); LUMINOUS_INTENSITY = Dimension(J=1); VELOCITY = Dimension(L=1, T=-1); DENSITY = Dimension(M=1, L=-3); ACCELERATION = Dimension(L=1, T=-2); FORCE = Dimension(M=1, L=1, T=-2)
AREA = LENGTH**2; FLOW_RATE = (LENGTH**3)/TIME; MASS_FLOW = MASS/TIME; PRESSURE = MASS/(LENGTH*(TIME**2)); POWER = (MASS*(LENGTH**2))/(TIME**3); SPECIFIC_HEAT = (LENGTH**2)/(TIME**2)/TEMPERATURE; HEAT_RATE = POWER; DYNAMIC_VISCOSITY = MASS/(LENGTH*TIME)
meter = Unit("meter", "m", LENGTH); centimeter = Unit("centimeter", "cm", LENGTH, 0.01); celsius = Unit("celsius", "°C", TEMPERATURE); kilogram = Unit("kilogram", "kg", MASS); second = Unit("second", "s", TIME); ampere = Unit("ampere", "A", CURRENT); kelvin = Unit("kelvin", "K", TEMPERATURE, offset=273.15); mole = Unit("mole", "mol", AMOUNT); candela = Unit("candela", "cd", LUMINOUS_INTENSITY)

def convert_unit(value, source, target):
    if source.dimension != target.dimension: raise ValueError("Cannot convert between different dimensions")
    if source == target: return value
    base_value = (value - source.offset) * source.scale_factor
    return target.offset + (base_value / target.scale_factor)

__all__ = [name for name in globals() if not name.startswith("_")]
