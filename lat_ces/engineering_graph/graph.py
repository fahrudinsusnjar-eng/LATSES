"""Canonical provenance graph connecting BuildingModel inputs to engineering layers.

The graph is intentionally evidence-oriented: it stores references and lineage,
not engineering decisions. Nodes and edges are append-only from the graph API's
perspective; a new fact/result should create a new node and relate it to prior
nodes rather than overwrite them.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from uuid import uuid4


class NodeKind(str, Enum):
    BUILDING_MODEL = "building_model"
    GEOMETRY = "geometry"
    PRODUCT = "product"
    FACT = "fact"
    ENVIRONMENT = "environment"
    EVIDENCE = "historical_evidence"
    CONSTRUCTION = "construction"
    LOAD = "load"
    ENGINEERING_MODEL = "engineering_model"
    RESULT = "result"


@dataclass(frozen=True)
class GraphNode:
    node_id: str
    kind: NodeKind
    source_ref: str
    version_ref: str = ""
    recorded_at: str = ""
    status: str = "active"
    metadata: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True)
class GraphEdge:
    edge_id: str
    source_node_id: str
    target_node_id: str
    relation: str
    recorded_at: str = ""
    metadata: tuple[tuple[str, str], ...] = ()


@dataclass
class EngineeringInputGraph:
    """Append-only lineage graph; does not mutate source records."""

    nodes: list[GraphNode] = field(default_factory=list)
    edges: list[GraphEdge] = field(default_factory=list)

    def add_node(
        self,
        kind: NodeKind,
        source_ref: str,
        *,
        version_ref: str = "",
        recorded_at: str = "",
        status: str = "active",
        metadata: dict[str, str] | None = None,
    ) -> GraphNode:
        if not source_ref.strip():
            raise ValueError("source_ref must not be empty")
        node = GraphNode(
            node_id=f"NODE-{uuid4()}",
            kind=kind,
            source_ref=source_ref,
            version_ref=version_ref,
            recorded_at=recorded_at,
            status=status,
            metadata=tuple(sorted((metadata or {}).items())),
        )
        self.nodes.append(node)
        return node

    def add_edge(
        self,
        source_node_id: str,
        target_node_id: str,
        relation: str,
        *,
        recorded_at: str = "",
        metadata: dict[str, str] | None = None,
    ) -> GraphEdge:
        if not relation.strip():
            raise ValueError("relation must not be empty")
        known = {node.node_id for node in self.nodes}
        if source_node_id not in known or target_node_id not in known:
            raise ValueError("both edge endpoints must already exist")
        edge = GraphEdge(
            edge_id=f"EDGE-{uuid4()}",
            source_node_id=source_node_id,
            target_node_id=target_node_id,
            relation=relation,
            recorded_at=recorded_at,
            metadata=tuple(sorted((metadata or {}).items())),
        )
        self.edges.append(edge)
        return edge

    def nodes_for_source(self, source_ref: str) -> tuple[GraphNode, ...]:
        return tuple(node for node in self.nodes if node.source_ref == source_ref)

    def incoming(self, node_id: str) -> tuple[GraphEdge, ...]:
        return tuple(edge for edge in self.edges if edge.target_node_id == node_id)

    def outgoing(self, node_id: str) -> tuple[GraphEdge, ...]:
        return tuple(edge for edge in self.edges if edge.source_node_id == node_id)

    def validate(self) -> list[str]:
        findings: list[str] = []
        node_ids = [node.node_id for node in self.nodes]
        if len(node_ids) != len(set(node_ids)):
            findings.append("Duplicate node_id detected")
        for edge in self.edges:
            if edge.source_node_id not in node_ids:
                findings.append(f"Missing source node for edge {edge.edge_id}")
            if edge.target_node_id not in node_ids:
                findings.append(f"Missing target node for edge {edge.edge_id}")
        return findings
