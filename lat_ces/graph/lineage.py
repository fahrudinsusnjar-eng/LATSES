"""Canonical, append-only engineering input lineage graph.

The graph links existing source records without copying or mutating them. Every
node and edge carries identity, version, source and time so downstream models
can reconstruct where an input came from and which historical state was used.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4


class Relation(str, Enum):
    DERIVED_FROM = "derived_from"
    VERIFIED_BY = "verified_by"
    SUPERSEDES = "supersedes"
    USED_BY = "used_by"


@dataclass(frozen=True)
class LineageNode:
    node_id: str
    node_type: str
    identity: str
    version: str
    source: str
    recorded_at: datetime
    valid_from: datetime | None = None
    valid_until: datetime | None = None
    metadata: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True)
class LineageEdge:
    edge_id: str
    relation: Relation
    from_node: str
    to_node: str
    source: str
    recorded_at: datetime
    valid_from: datetime | None = None
    valid_until: datetime | None = None
    metadata: tuple[tuple[str, str], ...] = ()


@dataclass
class EngineeringInputGraph:
    nodes: dict[str, LineageNode] = field(default_factory=dict)
    edges: dict[str, LineageEdge] = field(default_factory=dict)

    def add_node(self, node: LineageNode) -> LineageNode:
        if node.node_id in self.nodes:
            raise ValueError(f"Lineage node already exists: {node.node_id}")
        self.nodes[node.node_id] = node
        return node

    def add_edge(self, edge: LineageEdge) -> LineageEdge:
        if edge.edge_id in self.edges:
            raise ValueError(f"Lineage edge already exists: {edge.edge_id}")
        if edge.from_node not in self.nodes or edge.to_node not in self.nodes:
            raise KeyError("lineage edge references an unknown node")
        self.edges[edge.edge_id] = edge
        return edge

    def append_node(
        self,
        *,
        node_type: str,
        identity: str,
        version: str,
        source: str,
        recorded_at: datetime | None = None,
        valid_from: datetime | None = None,
        valid_until: datetime | None = None,
        metadata: tuple[tuple[str, str], ...] = (),
    ) -> LineageNode:
        node = LineageNode(
            node_id=f"NODE-{uuid4()}",
            node_type=node_type,
            identity=identity,
            version=version,
            source=source,
            recorded_at=recorded_at or datetime.now(timezone.utc),
            valid_from=valid_from,
            valid_until=valid_until,
            metadata=metadata,
        )
        return self.add_node(node)

    def append_edge(
        self,
        *,
        relation: Relation,
        from_node: str,
        to_node: str,
        source: str,
        recorded_at: datetime | None = None,
        valid_from: datetime | None = None,
        valid_until: datetime | None = None,
        metadata: tuple[tuple[str, str], ...] = (),
    ) -> LineageEdge:
        edge = LineageEdge(
            edge_id=f"EDGE-{uuid4()}",
            relation=relation,
            from_node=from_node,
            to_node=to_node,
            source=source,
            recorded_at=recorded_at or datetime.now(timezone.utc),
            valid_from=valid_from,
            valid_until=valid_until,
            metadata=metadata,
        )
        return self.add_edge(edge)

    def history(self, node_id: str) -> tuple[LineageNode, ...]:
        if node_id not in self.nodes:
            raise KeyError(node_id)
        superseded = {
            edge.from_node
            for edge in self.edges.values()
            if edge.relation == Relation.SUPERSEDES and edge.to_node == node_id
        }
        history = [self.nodes[node_id]]
        while superseded:
            current_id = superseded.pop()
            history.append(self.nodes[current_id])
            superseded = {
                edge.from_node
                for edge in self.edges.values()
                if edge.relation == Relation.SUPERSEDES and edge.to_node == current_id
            }
        return tuple(history)

    def upstream(self, node_id: str) -> tuple[LineageNode, ...]:
        if node_id not in self.nodes:
            raise KeyError(node_id)
        ids = {edge.from_node for edge in self.edges.values() if edge.to_node == node_id}
        return tuple(self.nodes[item] for item in ids)

    def downstream(self, node_id: str) -> tuple[LineageNode, ...]:
        if node_id not in self.nodes:
            raise KeyError(node_id)
        ids = {edge.to_node for edge in self.edges.values() if edge.from_node == node_id}
        return tuple(self.nodes[item] for item in ids)
