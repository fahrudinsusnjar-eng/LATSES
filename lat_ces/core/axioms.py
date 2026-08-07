"""
LAT-CES Core: Constitutional Axioms (CAX)
Dokumenti: LAT-CES-0001 do LAT-CES-0003
"""

from dataclasses import dataclass
from enum import Enum


class AuthorityLevel(Enum):
    PHYSICAL_REALITY = 1
    MATHEMATICAL_MODEL = 2
    SOFTWARE_ENGINE = 3
    AI_ASSISTANT = 4


@dataclass(frozen=True)
class Axiom:
    """A minimal immutable constitutional axiom representation."""

    name: str
    statement: str


class ConstitutionalAxiom:
    """Core constitutional axiom helpers and authority rules."""

    AXIOM_1_REALITY_SUPREMACY = (
        "Fizička realnost i mjerenja imaju apsolutni autoritet nad modelima."
    )
    AXIOM_7_TRACEABILITY = (
        "Svaka inženjerska odluka i objekt mora imati potpuni kriptografski dokaz porijekla."
    )

    @staticmethod
    def validate_authority(higher: AuthorityLevel, lower: AuthorityLevel) -> bool:
        """Ensure a lower authority cannot override a higher one."""
        return higher.value < lower.value


class ConstitutionalAxioms:
    """Static collection of foundational axioms."""

    @staticmethod
    def all() -> list[Axiom]:
        return [
            Axiom("identity", "A system is itself."),
            Axiom("consistency", "A system should not contradict itself."),
            Axiom("reality_supremacy", ConstitutionalAxiom.AXIOM_1_REALITY_SUPREMACY),
            Axiom("traceability", ConstitutionalAxiom.AXIOM_7_TRACEABILITY),
        ]
