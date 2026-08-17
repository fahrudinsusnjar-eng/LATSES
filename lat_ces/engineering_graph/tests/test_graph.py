from lat_ces.engineering_graph import EngineeringInputGraph, NodeKind


def test_graph_tracks_canonical_input_lineage_without_overwriting_history():
    graph = EngineeringInputGraph()
    building = graph.add_node(NodeKind.BUILDING_MODEL, "BLDG-001", version_ref="v1", recorded_at="2026-08-16")
    geometry = graph.add_node(NodeKind.GEOMETRY, "LEVEL-001/FLOORPLAN", version_ref="v3")
    product = graph.add_node(NodeKind.PRODUCT, "PROD-POROTHERM-X25", version_ref="v7")
    fact = graph.add_node(NodeKind.FACT, "PROD-POROTHERM-X25/density", version_ref="fact-2026")
    environment = graph.add_node(NodeKind.ENVIRONMENT, "SITE-001/climate", version_ref="climate-2026")
    evidence = graph.add_node(NodeKind.EVIDENCE, "SITE-001/historical", version_ref="evidence-01")
    load = graph.add_node(NodeKind.LOAD, "LOAD-001", version_ref="v1")
    structural = graph.add_node(NodeKind.ENGINEERING_MODEL, "STRUCTURAL-001", version_ref="v1")

    graph.add_edge(building.node_id, geometry.node_id, "defines")
    graph.add_edge(product.node_id, fact.node_id, "declares")
    graph.add_edge(fact.node_id, load.node_id, "supplies")
    graph.add_edge(environment.node_id, load.node_id, "conditions")
    graph.add_edge(evidence.node_id, load.node_id, "contextualizes")
    graph.add_edge(geometry.node_id, load.node_id, "quantifies")
    graph.add_edge(load.node_id, structural.node_id, "feeds")

    assert graph.validate() == []
    assert len(graph.nodes) == 8
    assert len(graph.edges) == 7
    assert graph.incoming(load.node_id)[-1].relation == "quantifies" or any(
        edge.relation == "conditions" for edge in graph.incoming(load.node_id)
    )


def test_new_version_is_append_only():
    graph = EngineeringInputGraph()
    old = graph.add_node(NodeKind.FACT, "PROD-1/density", version_ref="2026")
    new = graph.add_node(NodeKind.FACT, "PROD-1/density", version_ref="2036", status="supersedes")
    graph.add_edge(new.node_id, old.node_id, "supersedes")

    assert len(graph.nodes_for_source("PROD-1/density")) == 2
    assert old.version_ref == "2026"
    assert new.version_ref == "2036"
    assert graph.outgoing(new.node_id)[0].relation == "supersedes"
