"""Read-only projections of the canonical EngineeringInputGraph.

Engineering domains consume the same immutable snapshot and never mutate or
materialize copies of the source records.
"""
from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Iterable, Mapping

from lat_ces.engineering_graph.graph import EngineeringInputGraph, GraphEdge, GraphNode, NodeKind


@dataclass(frozen=True)
class DomainLineageSnapshot:
    nodes: tuple[GraphNode, ...]
    edges: tuple[GraphEdge, ...]


@dataclass(frozen=True)
class DomainReadView:
    domain: str
    snapshot: DomainLineageSnapshot

    @property
    def nodes(self) -> tuple[GraphNode, ...]:
        return self.snapshot.nodes

    @property
    def edges(self) -> tuple[GraphEdge, ...]:
        return self.snapshot.edges

    def find_kind(self, kind: NodeKind) -> tuple[GraphNode, ...]:
        return tuple(node for node in self.nodes if node.kind == kind)

    def incoming(self, node_id: str) -> tuple[GraphEdge, ...]:
        return tuple(edge for edge in self.edges if edge.target_node_id == node_id)

    def outgoing(self, node_id: str) -> tuple[GraphEdge, ...]:
        return tuple(edge for edge in self.edges if edge.source_node_id == node_id)


def _snapshot(graph: EngineeringInputGraph) -> DomainLineageSnapshot:
    return DomainLineageSnapshot(nodes=tuple(graph.nodes), edges=tuple(graph.edges))


def domain_views(graph: EngineeringInputGraph) -> Mapping[str, DomainReadView]:
    """Return three domain views over one immutable lineage snapshot."""
    snapshot = _snapshot(graph)
    views = {
        domain: DomainReadView(domain=domain, snapshot=snapshot)
        for domain in ("structural", "fluid", "thermal")
    }
    return MappingProxyType(views)
