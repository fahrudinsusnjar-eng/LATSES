from lat_ces.engineering_graph.graph import EngineeringInputGraph, NodeKind
from lat_ces.engineering_graph.readonly import readonly_projection


def test_readonly_projection_is_snapshot_and_traceable():
    graph = EngineeringInputGraph()
    building = graph.add_node(NodeKind.BUILDING_MODEL, "BLDG-1", version_ref="1")
    load = graph.add_node(NodeKind.LOAD, "LOAD-1", version_ref="1")
    graph.add_edge(building.node_id, load.node_id, "derived_from")

    view = readonly_projection(graph)

    assert view.by_kind("building_model") == (building,)
    assert view.upstream(load.node_id) == (building,)
    assert view.downstream(building.node_id) == (load,)

    graph.add_node(NodeKind.ENVIRONMENT, "ENV-1", version_ref="2")
    assert len(view.nodes) == 2


def test_readonly_projection_exposes_no_mutation_api():
    graph = EngineeringInputGraph()
    graph.add_node(NodeKind.BUILDING_MODEL, "BLDG-1")
    view = readonly_projection(graph)

    assert not hasattr(view, "add_node")
    assert not hasattr(view, "add_edge")
