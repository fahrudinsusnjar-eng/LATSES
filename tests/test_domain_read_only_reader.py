from dataclasses import FrozenInstanceError

import pytest

from lat_ces.domains.read_only_reader import domain_views
from lat_ces.engineering_graph.graph import EngineeringInputGraph, NodeKind


def _graph() -> EngineeringInputGraph:
    graph = EngineeringInputGraph()
    graph.add_node(NodeKind.BUILDING_MODEL, "BLDG-1", version_ref="12")
    graph.add_node(NodeKind.LOAD, "LOAD-1", version_ref="1")
    return graph


def test_all_domains_share_one_snapshot():
    views = domain_views(_graph())
    assert set(views) == {"structural", "fluid", "thermal"}
    assert views["structural"].snapshot is views["fluid"].snapshot
    assert views["fluid"].snapshot is views["thermal"].snapshot


def test_snapshot_is_detached_from_later_graph_mutation():
    graph = _graph()
    views = domain_views(graph)
    count = len(views["structural"].nodes)
    graph.add_node(NodeKind.ENVIRONMENT, "site:44:16")
    assert len(views["structural"].nodes) == count


def test_domain_view_has_no_write_api():
    view = domain_views(_graph())["structural"]
    for name in ("add_node", "append_node", "add_edge", "append_edge", "save", "write", "update", "delete"):
        with pytest.raises(AttributeError):
            getattr(view, name)


def test_domain_view_is_immutable():
    snapshot = domain_views(_graph())["thermal"].snapshot
    with pytest.raises(FrozenInstanceError):
        snapshot.nodes = ()
