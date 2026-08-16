"""Builders that expose existing engineering inputs through the provenance graph."""
from __future__ import annotations

from .graph import EngineeringInputGraph, NodeKind


def build_input_graph(
    graph: EngineeringInputGraph | None = None,
    *,
    building_ref: str,
    geometry_refs: tuple[str, ...] = (),
    product_refs: tuple[str, ...] = (),
    fact_refs: tuple[str, ...] = (),
    environment_refs: tuple[str, ...] = (),
    evidence_refs: tuple[str, ...] = (),
    construction_refs: tuple[str, ...] = (),
    load_refs: tuple[str, ...] = (),
    engineering_model_refs: tuple[str, ...] = (),
) -> EngineeringInputGraph:
    """Create lineage nodes without mutating any source model or record."""
    graph = graph or EngineeringInputGraph()
    building = graph.add_node(NodeKind.BUILDING_MODEL, building_ref)

    def add_group(refs: tuple[str, ...], kind: NodeKind, relation: str) -> None:
        for ref in refs:
            node = graph.add_node(kind, ref)
            graph.add_edge(building.node_id, node.node_id, relation)

    add_group(geometry_refs, NodeKind.GEOMETRY, "defines")
    add_group(product_refs, NodeKind.PRODUCT, "references")
    add_group(fact_refs, NodeKind.FACT, "uses_fact")
    add_group(environment_refs, NodeKind.ENVIRONMENT, "uses_environment")
    add_group(evidence_refs, NodeKind.EVIDENCE, "uses_evidence")
    add_group(construction_refs, NodeKind.CONSTRUCTION, "contains_construction")
    add_group(load_refs, NodeKind.LOAD, "produces_load_input")
    add_group(engineering_model_refs, NodeKind.ENGINEERING_MODEL, "feeds_engineering_model")
    return graph
