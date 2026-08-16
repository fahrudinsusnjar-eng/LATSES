import pytest

from lat_ces.domains.engineering_readers import (
    FluidInputReader,
    StructuralInputReader,
    ThermalInputReader,
)
from lat_ces.domains.read_only import domain_views
from lat_ces.engineering_graph import EngineeringInputGraph, NodeKind


def _views():
    graph = EngineeringInputGraph()
    for kind, ref in (
        (NodeKind.BUILDING_MODEL, "BLDG-1"),
        (NodeKind.GEOMETRY, "GEOM-1"),
        (NodeKind.LOAD, "LOAD-1"),
        (NodeKind.CONSTRUCTION, "ASSEMBLY-1"),
        (NodeKind.PRODUCT, "PROD-1"),
        (NodeKind.FACT, "FACT-1"),
        (NodeKind.ENVIRONMENT, "SITE-1"),
        (NodeKind.EVIDENCE, "EVID-1"),
    ):
        graph.add_node(kind, ref)
    return domain_views(graph)


def test_all_domains_consume_the_same_immutable_snapshot():
    views = _views()
    structural = StructuralInputReader().read(views["structural"])
    fluid = FluidInputReader().read(views["fluid"])
    thermal = ThermalInputReader().read(views["thermal"])

    assert structural.snapshot is fluid.snapshot is thermal.snapshot
    assert structural.domain == "structural"
    assert fluid.domain == "fluid"
    assert thermal.domain == "thermal"


def test_required_contract_is_explicit_per_domain():
    views = _views()
    structural = StructuralInputReader().read(views["structural"])
    fluid = FluidInputReader().read(views["fluid"])
    thermal = ThermalInputReader().read(views["thermal"])

    assert structural.required_kinds == (
        NodeKind.BUILDING_MODEL, NodeKind.GEOMETRY, NodeKind.LOAD
    )
    assert fluid.required_kinds == (
        NodeKind.BUILDING_MODEL, NodeKind.GEOMETRY
    )
    assert thermal.required_kinds == (
        NodeKind.BUILDING_MODEL, NodeKind.GEOMETRY, NodeKind.CONSTRUCTION
    )


def test_domain_cannot_read_when_a_required_graph_input_is_missing():
    graph = EngineeringInputGraph()
    graph.add_node(NodeKind.BUILDING_MODEL, "BLDG-1")
    graph.add_node(NodeKind.GEOMETRY, "GEOM-1")
    graph.add_node(NodeKind.CONSTRUCTION, "ASSEMBLY-1")
    views = domain_views(graph)

    with pytest.raises(ValueError, match="load"):
        StructuralInputReader().read(views["structural"])


def test_contract_resolves_unique_source_ref_without_copying_runtime_data():
    views = _views()
    contract = FluidInputReader().read(views["fluid"])

    node = contract.require_unique_source("GEOM-1", kind=NodeKind.GEOMETRY)
    assert node.source_ref == "GEOM-1"
    assert contract.source_refs(NodeKind.GEOMETRY) == ("GEOM-1",)


def test_duplicate_source_ref_is_rejected_as_ambiguous():
    graph = EngineeringInputGraph()
    graph.add_node(NodeKind.BUILDING_MODEL, "BLDG-1")
    graph.add_node(NodeKind.GEOMETRY, "GEOM-1")
    graph.add_node(NodeKind.GEOMETRY, "GEOM-1")
    views = domain_views(graph)

    contract = FluidInputReader().read(views["fluid"])
    with pytest.raises(ValueError, match="Multiple reader inputs"):
        contract.require_unique_source("GEOM-1", kind=NodeKind.GEOMETRY)
