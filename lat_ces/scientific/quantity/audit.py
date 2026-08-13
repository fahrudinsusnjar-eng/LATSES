"""Scientific audit records for physical-quantity changes."""
from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class AuditRecord:
    object_id: str
    action: str
    previous_revision: str | None
    new_revision: str
    actor: str
    timestamp: str
    evidence: str | None = None


def create_audit(quantity, action: str, previous_revision: str | None = None, actor: str = "SYSTEM", evidence: str | None = None):
    return AuditRecord(
        object_id=quantity.quantity_id,
        action=action,
        previous_revision=previous_revision,
        new_revision=quantity.revision,
        actor=actor,
        timestamp=datetime.now(timezone.utc).isoformat(),
        evidence=evidence,
    )
