from datetime import datetime, timezone

from lat_ces.graph import EngineeringInputGraph, Relation


def test_lineage_nodes_and_edges_are_append_only_and_traceable():
    graph = EngineeringInputGraph()
    t0 = datetime(2026, 8, 16, tzinfo=timezone.utc)
    building = graph.append_node(
        node_type="building_model",
        identity="BLDG-1",
        version="12",
        source="building-model",
        recorded_at=t0,
    )
    fact_old = graph.append_node(
        node_type="technical_fact",
        identity="PRODUCT-1:density",
        version="2026.1",
        source="manufacturer-datasheet",
        recorded_at=t0,
        valid_from=t0,
    )
    fact_new = graph.append_node(
        node_type="technical_fact",
        identity="PRODUCT-1:density",
        version="2030.1",
        source="manufacturer-datasheet",
        recorded_at=datetime(2030, 1, 1, tzinfo=timezone.utc),
        valid_from=datetime(2030, 1, 1, tzinfo=timezone.utc),
    )
    load = graph.append_node(
        node_type="load_ledger",
        identity="LOAD-1",
        version="1",
        source="load-builder",
        recorded_at=t0,
    )

    graph.append_edge(
        relation=Relation.DERIVED_FROM,
        from_node=fact_old.node_id,
        to_node=load.node_id,
        source="load-builder",
        recorded_at=t0,
    )
    graph.append_edge(
        relation=Relation.USED_BY,
        from_node=building.node_id,
        to_node=load.node_id,
        source="structural-input-adapter",
        recorded_at=t0,
    )
    graph.append_edge(
        relation=Relation.SUPERSEDES,
        from_node=fact_new.node_id,
        to_node=fact_old.node_id,
        source="verification-loop",
        recorded_at=datetime(2030, 1, 1, tzinfo=timezone.utc),
    )

    assert len(graph.nodes) == 4
    assert len(graph.edges) == 3
    assert graph.history(fact_old.node_id) == (fact_old, fact_new)
    assert {node.node_id for node in graph.upstream(load.node_id)} == {fact_old.node_id, building.node_id}


def test_lineage_rejects_edges_to_unknown_nodes():
    graph = EngineeringInputGraph()
    node = graph.append_node(
        node_type="building_model",
        identity="BLDG-1",
        version="1",
        source="building-model",
    )
    try:
        graph.append_edge(
            relation=Relation.USED_BY,
            from_node=node.node_id,
            to_node="NODE-missing",
            source="test",
        )
    except KeyError:
        return
    raise AssertionError("lineage edge must reference existing nodes")
