import pytest

from lat_ces.domains.engineering_readers import (
    FluidInputReader,
    StructuralInputReader,
    ThermalInputReader,
    read_domain_inputs,
)
from lat_ces.domains.read_only import domain_views
from lat_ces.engineering_graph.graph import EngineeringInputGraph, NodeKind


def _views():
    graph = EngineeringInputGraph()
    graph.add_node(NodeKind.BUILDING_MODEL, "BLDG-1", version_ref="12")
    graph.add_node(NodeKind.GEOMETRY, "GEOM-1", version_ref="3")
    graph.add_node(NodeKind.PRODUCT, "PROD-1", version_ref="2")
    graph.add_node(NodeKind.FACT, "FACT-1", version_ref="verified")
    graph.add_node(NodeKind.ENVIRONMENT, "SITE-1", version_ref="4")
    graph.add_node(NodeKind.EVIDENCE, "EVID-1", version_ref="1")
    graph.add_node(NodeKind.CONSTRUCTION, "ASSEMBLY-1", version_ref="5")
    graph.add_node(NodeKind.LOAD, "LOAD-1", version_ref="6")
    return domain_views(graph)


def test_structural_reader_uses_shared_snapshot_and_loads_load_inputs():
    view = _views()["structural"]
    result = StructuralInputReader().read(view)
    assert result.snapshot is view.snapshot
    assert "LOAD-1" in result.source_refs()
    assert "GEOM-1" in result.source_refs()


def test_fluid_reader_uses_shared_snapshot_without_structural_load_copy():
    view = _views()["fluid"]
    result = FluidInputReader().read(view)
    assert result.snapshot is view.snapshot
    assert "GEOM-1" in result.source_refs()
    assert "LOAD-1" not in result.source_refs()


def test_thermal_reader_uses_shared_snapshot_without_load_copy():
    view = _views()["thermal"]
    result = ThermalInputReader().read(view)
    assert result.snapshot is view.snapshot
    assert "ASSEMBLY-1" in result.source_refs()
    assert "LOAD-1" not in result.source_refs()


def test_dispatch_rejects_cross_domain_reader_use():
    views = _views()
    with pytest.raises(ValueError):
        StructuralInputReader().read(views["fluid"])
    with pytest.raises(ValueError):
        read_domain_inputs(type("View", (), {"domain": "unknown", "snapshot": views["thermal"].snapshot})())
