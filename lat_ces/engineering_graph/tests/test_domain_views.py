from lat_ces.engineering_graph.domain_views import fluid_inputs, structural_inputs, thermal_inputs
from lat_ces.engineering_graph.graph import EngineeringInputGraph, NodeKind
from lat_ces.engineering_graph.readonly import readonly_projection


def test_all_domain_views_share_same_read_only_snapshot():
    graph = EngineeringInputGraph()
    graph.add_node(NodeKind.BUILDING_MODEL, "BLDG-1")
    view = readonly_projection(graph)

    structural = structural_inputs(view)
    fluid = fluid_inputs(view)
    thermal = thermal_inputs(view)

    assert structural.nodes is view.nodes
    assert fluid.nodes is view.nodes
    assert thermal.nodes is view.nodes
    assert structural.edges is fluid.edges is thermal.edges
