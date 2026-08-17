"""Read-only Structural/Fluid/Thermal readers over one shared graph snapshot."""
from __future__ import annotations

from .read_only import ReadOnlyDomainView
from .reader_contract import EngineeringReaderContract
from lat_ces.engineering_graph.graph import NodeKind


class _DomainReader:
    DOMAIN: str = ""
    REQUIRED_KINDS: tuple[NodeKind, ...] = ()
    OPTIONAL_KINDS: tuple[NodeKind, ...] = ()

    def read(self, view: ReadOnlyDomainView) -> EngineeringReaderContract:
        if view.domain != self.DOMAIN:
            raise ValueError(f"Reader '{self.DOMAIN}' cannot consume domain '{view.domain}'")
        contract = EngineeringReaderContract(
            domain=self.DOMAIN,
            snapshot=view.snapshot,
            required_kinds=self.REQUIRED_KINDS,
            optional_kinds=self.OPTIONAL_KINDS,
        )
        findings = contract.validate_contract()
        if findings:
            raise ValueError("; ".join(findings))
        return contract


class StructuralInputReader(_DomainReader):
    DOMAIN = "structural"
    REQUIRED_KINDS = (
        NodeKind.BUILDING_MODEL,
        NodeKind.GEOMETRY,
        NodeKind.LOAD,
    )
    OPTIONAL_KINDS = (
        NodeKind.PRODUCT,
        NodeKind.FACT,
        NodeKind.ENVIRONMENT,
        NodeKind.EVIDENCE,
        NodeKind.CONSTRUCTION,
    )


class FluidInputReader(_DomainReader):
    DOMAIN = "fluid"
    REQUIRED_KINDS = (
        NodeKind.BUILDING_MODEL,
        NodeKind.GEOMETRY,
    )
    OPTIONAL_KINDS = (
        NodeKind.PRODUCT,
        NodeKind.FACT,
        NodeKind.ENVIRONMENT,
        NodeKind.CONSTRUCTION,
    )


class ThermalInputReader(_DomainReader):
    DOMAIN = "thermal"
    REQUIRED_KINDS = (
        NodeKind.BUILDING_MODEL,
        NodeKind.GEOMETRY,
        NodeKind.CONSTRUCTION,
    )
    OPTIONAL_KINDS = (
        NodeKind.PRODUCT,
        NodeKind.FACT,
        NodeKind.ENVIRONMENT,
    )


def read_domain_inputs(view: ReadOnlyDomainView) -> EngineeringReaderContract:
    readers = {
        "structural": StructuralInputReader(),
        "fluid": FluidInputReader(),
        "thermal": ThermalInputReader(),
    }
    try:
        reader = readers[view.domain]
    except KeyError as exc:
        raise ValueError(f"Unsupported engineering domain: {view.domain}") from exc
    return reader.read(view)
