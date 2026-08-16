"""Read-only engineering domain readers over the shared input snapshot."""
from __future__ import annotations

from dataclasses import dataclass

from .read_only import EngineeringInputSnapshot, ReadOnlyDomainView
from lat_ces.engineering_graph.graph import NodeKind, GraphNode


@dataclass(frozen=True)
class DomainInput:
    domain: str
    snapshot: EngineeringInputSnapshot
    nodes: tuple[GraphNode, ...]

    def source_refs(self) -> tuple[str, ...]:
        return tuple(node.source_ref for node in self.nodes)


class _DomainReader:
    DOMAIN: str = ""
    KINDS: tuple[NodeKind, ...] = ()

    def read(self, view: ReadOnlyDomainView) -> DomainInput:
        if view.domain != self.DOMAIN:
            raise ValueError(f"Reader '{self.DOMAIN}' cannot consume domain '{view.domain}'")
        nodes = tuple(node for node in view.snapshot.nodes if node.kind in self.KINDS)
        return DomainInput(domain=self.DOMAIN, snapshot=view.snapshot, nodes=nodes)


class StructuralInputReader(_DomainReader):
    DOMAIN = "structural"
    KINDS = (
        NodeKind.BUILDING_MODEL,
        NodeKind.GEOMETRY,
        NodeKind.PRODUCT,
        NodeKind.FACT,
        NodeKind.ENVIRONMENT,
        NodeKind.EVIDENCE,
        NodeKind.CONSTRUCTION,
        NodeKind.LOAD,
    )


class FluidInputReader(_DomainReader):
    DOMAIN = "fluid"
    KINDS = (
        NodeKind.BUILDING_MODEL,
        NodeKind.GEOMETRY,
        NodeKind.PRODUCT,
        NodeKind.FACT,
        NodeKind.ENVIRONMENT,
        NodeKind.CONSTRUCTION,
    )


class ThermalInputReader(_DomainReader):
    DOMAIN = "thermal"
    KINDS = (
        NodeKind.BUILDING_MODEL,
        NodeKind.GEOMETRY,
        NodeKind.PRODUCT,
        NodeKind.FACT,
        NodeKind.ENVIRONMENT,
        NodeKind.CONSTRUCTION,
    )


def read_domain_inputs(view: ReadOnlyDomainView) -> DomainInput:
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
