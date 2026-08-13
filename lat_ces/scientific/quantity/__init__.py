"""LAT-CES Scientific Physical Quantity hardening layer (SCI 42-45)."""

from .quantity import HardenedPhysicalQuantity
from .equation import Equation
from .measurement import MeasurementTrace
from .integrity import generate_quantity_hash, generate_equation_hash, verify_quantity_integrity
from .revision import QuantityRevisionManager, RevisionRecord
from .audit import AuditRecord, create_audit
from .evidence import EvidenceLink
from .validation import validate_hardened_quantity

__all__ = [
    "HardenedPhysicalQuantity",
    "Equation",
    "MeasurementTrace",
    "generate_quantity_hash",
    "generate_equation_hash",
    "verify_quantity_integrity",
    "QuantityRevisionManager",
    "RevisionRecord",
    "AuditRecord",
    "create_audit",
    "EvidenceLink",
    "validate_hardened_quantity",
]
