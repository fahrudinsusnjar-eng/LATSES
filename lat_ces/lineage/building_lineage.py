"""Canonical assembly of the Building Model engineering input lineage.

This adapter only links existing records. It does not mutate source histories.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable

from lat_ces.building.model import BuildingModel
from lat_ces.building.environment import SiteEnvironment
from lat_ces.evidence.historical import HistoricalEvidenceLedger
from lat_ces.catalog.temporal import ProductIdentity, TechnicalFact, VerificationRecord
from lat_ces.structural.load_ledger import LoadLedger

from .graph import EngineeringInputGraph, LineageEdge, LineageNode


@dataclass(frozen=True)
class TechnicalCatalogSnapshot:
    products: tuple[ProductIdentity, ...] = ()
    facts: tuple[TechnicalFact, ...] = ()
    verifications: tuple[VerificationRecord, ...] = ()


def _node(node_id: str, kind: str, version: str, source: str, recorded_at: datetime) -> LineageNode:
    return LineageNode(
        node_id=node_id,
        kind=kind,
        version=version,
        source=source,
        recorded_at=recorded_at,
    )


def build_building_input_lineage(
    building: BuildingModel,
    catalog: TechnicalCatalogSnapshot,
    environment: SiteEnvironment,
    evidence: HistoricalEvidenceLedger,
    load_ledger: LoadLedger,
    *,
    recorded_at: datetime,
    version: str,
) -> EngineeringInputGraph:
    """Create a read-only lineage view over canonical engineering inputs."""
    graph = EngineeringInputGraph()

    building_node = _node(building.model_id, "building_model", version, "BuildingModel", recorded_at)
    graph.add_node(building_node)

    environment_node = _node(
        f"environment:{environment.latitude_deg}:{environment.longitude_deg}",
        "environment",
        version,
        "SiteEnvironment",
        recorded_at,
    )
    graph.add_node(environment_node)
    graph.add_edge(LineageEdge(building_node.node_id, environment_node.node_id, "derived_from", recorded_at))

    for product in catalog.products:
        product_node = _node(product.product_id, "technical_product", version, "TechnicalCatalog", recorded_at)
        graph.add_node(product_node)
        graph.add_edge(LineageEdge(product_node.node_id, building_node.node_id, "used_by", recorded_at))

        for fact in catalog.facts:
            if fact.product_id != product.product_id:
                continue
            fact_node = _node(fact.fact_id, "technical_fact", fact.state.value, fact.source_url, fact.observed_at)
            graph.add_node(fact_node)
            graph.add_edge(LineageEdge(fact_node.node_id, product_node.node_id, "derived_from", fact.observed_at))
            if fact.supersedes_fact_id:
                graph.add_edge(LineageEdge(fact.node_id if hasattr(fact, "node_id") else fact.fact_id, fact.supersedes_fact_id, "supersedes", fact.observed_at))
            for verification in catalog.verifications:
                if verification.fact_id == fact.fact_id:
                    verification_node = _node(
                        verification.verification_id,
                        "verification",
                        verification.result,
                        verification.source_url,
                        verification.checked_at,
                    )
                    graph.add_node(verification_node)
                    graph.add_edge(LineageEdge(fact.fact_id, verification_node.node_id, "verified_by", verification.checked_at))

    for record in evidence.records:
        evidence_node = _node(record.evidence_id, "historical_evidence", record.state.value, record.source, datetime.fromisoformat(record.recorded_at))
        graph.add_node(evidence_node)
        graph.add_edge(LineageEdge(evidence_node.node_id, building_node.node_id, "used_by", evidence_node.recorded_at))
        if record.supersedes:
            graph.add_edge(LineageEdge(evidence_node.node_id, record.supersedes, "supersedes", evidence_node.recorded_at))

    ledger_node = _node(f"load-ledger:{building.model_id}", "load_ledger", version, "LoadLedger", recorded_at)
    graph.add_node(ledger_node)
    graph.add_edge(LineageEdge(building_node.node_id, ledger_node.node_id, "derived_from", recorded_at))
    graph.add_edge(LineageEdge(environment_node.node_id, ledger_node.node_id, "derived_from", recorded_at))

    return graph
