"""Read-only domain projections over the canonical Engineering Input Graph."""
from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from lat_ces.engineering_graph.graph import EngineeringInputGraph, GraphEdge, GraphNode


@dataclass(frozen=True)
class EngineeringInputSnapshot:
    """Immutable snapshot shared by engineering domains."""

    nodes: tuple[GraphNode, ...]
    edges: tuple[GraphEdge, ...]

    @classmethod
    def from_graph(cls, graph: EngineeringInputGraph) -> "EngineeringInputSnapshot":
        return cls(nodes=tuple(graph.nodes), edges=tuple(graph.edges))

    def node(self, node_id: str) -> GraphNode:
        for node in self.nodes:
            if node.node_id == node_id:
                return node
        raise KeyError(node_id)

    def incoming(self, node_id: str) -> tuple[GraphEdge, ...]:
        return tuple(edge for edge in self.edges if edge.target_node_id == node_id)

    def outgoing(self, node_id: str) -> tuple[GraphEdge, ...]:
        return tuple(edge for edge in self.edges if edge.source_node_id == node_id)


@dataclass(frozen=True)
class ReadOnlyDomainView:
    """Common read-only contract for Structural, Fluid and Thermal domains."""

    domain: str
    snapshot: EngineeringInputSnapshot

    @property
    def nodes(self) -> tuple[GraphNode, ...]:
        return self.snapshot.nodes

    @property
    def edges(self) -> tuple[GraphEdge, ...]:
        return self.snapshot.edges

    def source_nodes(self, source_ref: str) -> tuple[GraphNode, ...]:
        return tuple(node for node in self.nodes if node.source_ref == source_ref)

    def __getattr__(self, name: str):
        if name in {"append_node", "add_node", "append_edge", "add_edge", "delete", "update", "save", "write"}:
            raise AttributeError(f"{self.__class__.__name__} is read-only; '{name}' is not available")
        raise AttributeError(name)


def domain_views(graph: EngineeringInputGraph) -> Mapping[str, ReadOnlyDomainView]:
    snapshot = EngineeringInputSnapshot.from_graph(graph)
    return MappingProxyType({
        domain: ReadOnlyDomainView(domain=domain, snapshot=snapshot)
        for domain in ("structural", "fluid", "thermal")
    })
