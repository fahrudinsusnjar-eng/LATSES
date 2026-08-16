"""Canonical contract shared by Structural, Fluid and Thermal input readers.

The contract is intentionally solver-neutral. It exposes one immutable graph
snapshot plus typed lineage selection helpers. Runtime engineering objects are
resolved later by domain-specific adapters; no calculator is invoked here.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from lat_ces.engineering_graph.graph import GraphNode, NodeKind
from .read_only import EngineeringInputSnapshot


@dataclass(frozen=True)
class EngineeringReaderContract:
    """Immutable reader output over one shared EngineeringInputGraph snapshot."""

    domain: str
    snapshot: EngineeringInputSnapshot
    required_kinds: tuple[NodeKind, ...]
    optional_kinds: tuple[NodeKind, ...]

    @property
    def nodes(self) -> tuple[GraphNode, ...]:
        return self.snapshot.nodes

    @property
    def edges(self):
        return self.snapshot.edges

    def by_kind(self, kind: NodeKind) -> tuple[GraphNode, ...]:
        return tuple(node for node in self.nodes if node.kind == kind)

    def require_kind(self, kind: NodeKind) -> tuple[GraphNode, ...]:
        matches = self.by_kind(kind)
        if not matches:
            raise ValueError(f"{self.domain} reader requires graph kind '{kind.value}'")
        return matches

    def require_unique_source(self, source_ref: str, *, kind: NodeKind | None = None) -> GraphNode:
        matches = tuple(
            node
            for node in self.nodes
            if node.source_ref == source_ref and (kind is None or node.kind == kind)
        )
        if not matches:
            suffix = f" and kind '{kind.value}'" if kind else ""
            raise KeyError(f"No reader input for source_ref '{source_ref}'{suffix}")
        if len(matches) > 1:
            raise ValueError(f"Multiple reader inputs for source_ref '{source_ref}'")
        return matches[0]

    def source_refs(self, kind: NodeKind | None = None) -> tuple[str, ...]:
        nodes: Iterable[GraphNode] = self.nodes if kind is None else self.by_kind(kind)
        return tuple(node.source_ref for node in nodes)

    def validate_contract(self) -> tuple[str, ...]:
        findings: list[str] = []
        available = {node.kind for node in self.nodes}
        missing = [kind.value for kind in self.required_kinds if kind not in available]
        if missing:
            findings.append(
                f"{self.domain} reader contract missing required kinds: {', '.join(missing)}"
            )
        return tuple(findings)
