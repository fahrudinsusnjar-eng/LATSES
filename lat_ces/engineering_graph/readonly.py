"""Read-only projection of the engineering input lineage for domain modules."""
from __future__ import annotations

from dataclasses import dataclass

from .graph import EngineeringInputGraph, GraphNode, GraphEdge


@dataclass(frozen=True)
class ReadOnlyEngineeringInputs:
    """Immutable view; domain solvers cannot mutate the source graph through it."""

    nodes: tuple[GraphNode, ...]
    edges: tuple[GraphEdge, ...]

    def by_kind(self, kind: str) -> tuple[GraphNode, ...]:
        return tuple(node for node in self.nodes if node.kind.value == kind)

    def upstream(self, node_id: str) -> tuple[GraphNode, ...]:
        source_ids = {
            edge.source_node_id
            for edge in self.edges
            if edge.target_node_id == node_id
        }
        return tuple(node for node in self.nodes if node.node_id in source_ids)

    def downstream(self, node_id: str) -> tuple[GraphNode, ...]:
        target_ids = {
            edge.target_node_id
            for edge in self.edges
            if edge.source_node_id == node_id
        }
        return tuple(node for node in self.nodes if node.node_id in target_ids)


def readonly_projection(graph: EngineeringInputGraph) -> ReadOnlyEngineeringInputs:
    """Create an immutable snapshot for Structural/Fluid/Thermal readers."""
    return ReadOnlyEngineeringInputs(
        nodes=tuple(graph.nodes),
        edges=tuple(graph.edges),
    )
