from __future__ import annotations

import hashlib
import json
import math
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional, Union

from lat_ces.core.dimensions import Unit, UnitSKOError


@dataclass(frozen=True)
class MeasurementTrace:
    value: float
    unit: Unit
    uncertainty: float
    method: str
    source: str


@dataclass(frozen=True)
class EvidenceLink:
    source: str


@dataclass(frozen=True)
class AuditRecord:
    object_id: str
    action: str
    previous_revision: Optional[str]
    new_revision: str
    actor: str
    timestamp: str
    evidence: Optional[str] = None


class PhysicalQuantityRevisionManager:
    def __init__(self):
        self.history = []

    def register(self, quantity, reason: str = "Initial definition"):
        record = {
            "quantity_id": quantity.quantity_id,
            "revision": quantity.revision,
            "reason": reason,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self.history.append(record)
        return record

    def latest(self):
        return self.history[-1] if self.history else None


class PhysicalQuantity:
    """Native physical quantity with uncertainty and SCI 42-45 hardening metadata."""

    def __init__(
        self,
        value: float,
        uncertainty: float,
        unit: Unit,
        confidence_level: float = 0.95,
        sko_uuid: Optional[str] = None,
        status: str = "DRAFT",
        *,
        quantity_id: Optional[str] = None,
        name: Optional[str] = None,
        symbol: Optional[str] = None,
        definition: str = "",
        equation: Optional[str] = None,
        revision: str = "A",
        measurement_model: Optional[MeasurementTrace] = None,
        evidence: Optional[EvidenceLink] = None,
    ):
        if uncertainty < 0.0:
            raise UnitSKOError("Mjerna neodređenost ne može biti negativna vrijednost.")
        if not isinstance(unit, Unit):
            raise UnitSKOError("Physical quantity mora biti vezana za validnu jedinicu.")
        if not revision:
            raise UnitSKOError("Revision ne može biti prazna.")

        self._value = float(value)
        self._uncertainty = float(uncertainty)
        self._unit = unit
        self._confidence_level = confidence_level
        self._uuid = sko_uuid or str(uuid.uuid4())
        self._status = status
        self._quantity_id = quantity_id or f"PQ-{self._uuid}"
        self._name = name or unit.name
        self._symbol = symbol or unit.symbol
        self._definition = definition
        self._equation = equation or ""
        self._revision = revision
        self._measurement_model = measurement_model
        self._evidence = evidence
        self._audit_log: list[AuditRecord] = []
        self._revision_history: list[dict] = []
        self._equation_hash = self._hash_text(self._equation)
        self._integrity_hash = self._compute_integrity_hash()

    @staticmethod
    def _hash_text(value: str) -> str:
        return hashlib.sha256(value.encode("utf-8")).hexdigest()

    def _compute_integrity_hash(self) -> str:
        data = {
            "quantity_id": self._quantity_id,
            "name": self._name,
            "symbol": self._symbol,
            "definition": self._definition,
            "dimension": str(self._unit.dimension),
            "unit": str(self._unit),
            "equation": self._equation,
        }
        return hashlib.sha256(json.dumps(data, sort_keys=True, default=str).encode("utf-8")).hexdigest()

    @property
    def value(self) -> float:
        return self._value

    @property
    def uncertainty(self) -> float:
        return self._uncertainty

    @property
    def relative_uncertainty(self) -> float:
        if self._value == 0.0:
            return 0.0 if self._uncertainty == 0.0 else float("inf")
        return abs(self._uncertainty / self._value)

    @property
    def unit(self) -> Unit:
        return self._unit

    @property
    def quantity_id(self) -> str:
        return self._quantity_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def symbol(self) -> str:
        return self._symbol

    @property
    def definition(self) -> str:
        return self._definition

    @property
    def equation(self) -> str:
        return self._equation

    @property
    def revision(self) -> str:
        return self._revision

    @property
    def integrity_hash(self) -> str:
        return self._integrity_hash

    @property
    def equation_hash(self) -> str:
        return self._equation_hash

    @property
    def measurement_model(self) -> Optional[MeasurementTrace]:
        return self._measurement_model

    @property
    def evidence(self) -> Optional[EvidenceLink]:
        return self._evidence

    @property
    def audit_log(self):
        return tuple(self._audit_log)

    @property
    def revision_history(self):
        return tuple(self._revision_history)

    def verify_integrity(self) -> bool:
        return self._compute_integrity_hash() == self._integrity_hash

    def add_audit(self, action: str, previous_revision: Optional[str] = None, actor: str = "SYSTEM", evidence: Optional[str] = None):
        record = AuditRecord(
            object_id=self._quantity_id,
            action=action,
            previous_revision=previous_revision,
            new_revision=self._revision,
            actor=actor,
            timestamp=datetime.now(timezone.utc).isoformat(),
            evidence=evidence,
        )
        self._audit_log.append(record)
        return record

    def create_revision(self, revision: str, *, definition: Optional[str] = None, equation: Optional[str] = None, reason: str = "Scientific revision"):
        if not revision or revision == self._revision:
            raise UnitSKOError("Nova revizija mora imati novi identifikator.")
        self._revision_history.append({"revision": self._revision, "definition": self._definition, "equation": self._equation})
        self._revision = revision
        if definition is not None:
            self._definition = definition
        if equation is not None:
            self._equation = equation
        self._equation_hash = self._hash_text(self._equation)
        self._integrity_hash = self._compute_integrity_hash()
        self.add_audit("REVISION", self._revision_history[-1]["revision"], evidence=reason)
        return self

    def validate_dimension_lock(self, expected_dimension) -> bool:
        if self._unit.dimension != expected_dimension:
            raise UnitSKOError("Dimension lock violated.")
        return True

    def __add__(self, other: "PhysicalQuantity") -> "PhysicalQuantity":
        if self._unit.dimension != other._unit.dimension:
            raise UnitSKOError(f"Dimenzionalna neslaganja: {self._unit.dimension} vs {other._unit.dimension}")
        other_converted_val = (other.value * other.unit.scale_factor) / self._unit.scale_factor
        other_converted_unc = (other.uncertainty * other.unit.scale_factor) / self._unit.scale_factor
        return PhysicalQuantity(self._value + other_converted_val, math.sqrt(self._uncertainty**2 + other_converted_unc**2), self._unit)

    def __mul__(self, other: Union["PhysicalQuantity", int, float]) -> "PhysicalQuantity":
        if isinstance(other, PhysicalQuantity):
            new_val = self._value * other.value
            new_unit = self._unit * other.unit
            new_unc = abs(new_val) * math.sqrt(self.relative_uncertainty**2 + other.relative_uncertainty**2)
            return PhysicalQuantity(new_val, new_unc, new_unit)
        if isinstance(other, (int, float)):
            scalar = float(other)
            return PhysicalQuantity(self._value * scalar, self._uncertainty * abs(scalar), self._unit)
        return NotImplemented

    def __truediv__(self, other: Union["PhysicalQuantity", int, float]) -> "PhysicalQuantity":
        if isinstance(other, PhysicalQuantity):
            if other.value == 0.0:
                raise ZeroDivisionError("Dijeljenje sa fizikalnom veličinom čija je vrijednost 0.0 nije dozvoljeno.")
            new_val = self._value / other.value
            new_unit = self._unit / other.unit
            new_unc = abs(new_val) * math.sqrt(self.relative_uncertainty**2 + other.relative_uncertainty**2)
            return PhysicalQuantity(new_val, new_unc, new_unit)
        if isinstance(other, (int, float)):
            scalar = float(other)
            if scalar == 0.0:
                raise ZeroDivisionError("Dijeljenje sa skalarom 0 nije dozvoljeno.")
            return PhysicalQuantity(self._value / scalar, self._uncertainty / abs(scalar), self._unit)
        return NotImplemented

    def __rtruediv__(self, other: Union[int, float]) -> "PhysicalQuantity":
        if isinstance(other, (int, float)):
            if self._value == 0.0:
                raise ZeroDivisionError("Dijeljenje skalara sa nulom nije dozvoljeno.")
            scalar = float(other)
            new_val = scalar / self._value
            new_unit = self._unit ** -1
            new_unc = abs(new_val) * self.relative_uncertainty
            return PhysicalQuantity(new_val, new_unc, new_unit)
        return NotImplemented

    def __pow__(self, exponent: Union[int, float]) -> "PhysicalQuantity":
        if not isinstance(exponent, (int, float)):
            return NotImplemented
        exp = float(exponent)
        new_val = self._value ** exp
        new_unit = self._unit ** exp
        new_unc = abs(new_val) * abs(exp) * self.relative_uncertainty
        return PhysicalQuantity(new_val, new_unc, new_unit)

    def sqrt(self) -> "PhysicalQuantity":
        return self ** 0.5

    def __repr__(self) -> str:
        return f"{self._value:.4f} ± {self._uncertainty:.4f} {self._unit.symbol} (u_rel: {self.relative_uncertainty * 100:.2f}%)"
