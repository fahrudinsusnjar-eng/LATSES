"""Canonical assembly of Building Model inputs into the engineering lineage."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from lat_ces.building.environment import SiteEnvironment
from lat_ces.building.model import BuildingModel
from lat_ces.catalog.temporal import ProductIdentity, TechnicalFact, VerificationRecord
from lat_ces.evidence.historical import HistoricalEvidenceLedger
from lat_ces.structural.load_ledger import LoadLedger

from lat_ces.engineering_graph.graph import EngineeringInputGraph, NodeKind


@dataclass(frozen=True)
class TechnicalCatalogSnapshot:
    products: tuple[ProductIdentity, ...] = ()
    facts: tuple[TechnicalFact, ...] = ()
    verifications: tuple[VerificationRecord, ...] = ()


def _add_node(
    graph: EngineeringInputGraph,
    *,
    kind: NodeKind,
    source_ref: str,
    version_ref: str,
    recorded_at: datetime,
    status: str = "active",
    metadata: dict[str, str] | None = None,
):
    return graph.add_node(
        kind,
        source_ref,
        version_ref=version_ref,
        recorded_at=recorded_at.isoformat(),
        status=status,
        metadata=metadata,
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
    """Build a read-only lineage graph over canonical engineering inputs."""
    graph = EngineeringInputGraph()

    building_node = _add_node(
        graph,
        kind=NodeKind.BUILDING_MODEL,
        source_ref=building.model_id,
        version_ref=version,
        recorded_at=recorded_at,
        metadata={"name": building.name},
    )

    environment_node = _add_node(
        graph,
        kind=NodeKind.ENVIRONMENT,
        source_ref=f"site:{environment.latitude_deg}:{environment.longitude_deg}",
        version_ref=version,
        recorded_at=recorded_at,
        metadata={"latitude_deg": str(environment.latitude_deg), "longitude_deg": str(environment.longitude_deg)},
    )
    graph.add_edge(building_node.node_id, environment_node.node_id, "derived_from", recorded_at=recorded_at.isoformat())

    product_nodes: dict[str, object] = {}
    for product in catalog.products:
        product_node = _add_node(
            graph,
            kind=NodeKind.PRODUCT,
            source_ref=product.product_id,
            version_ref=version,
            recorded_at=recorded_at,
            metadata={"manufacturer": product.manufacturer, "model_code": product.model_code},
        )
        product_nodes[product.product_id] = product_node
        graph.add_edge(product_node.node_id, building_node.node_id, "used_by", recorded_at=recorded_at.isoformat())

    fact_nodes: dict[str, object] = {}
    for fact in catalog.facts:
        fact_node = _add_node(
            graph,
            kind=NodeKind.FACT,
            source_ref=fact.fact_id,
            version_ref=fact.state.value,
            recorded_at=fact.observed_at,
            status=fact.state.value,
            metadata={
                "product_id": fact.product_id,
                "property_name": fact.property_name,
                "unit": fact.unit,
                "source_url": fact.source_url,
            },
        )
        fact_nodes[fact.fact_id] = fact_node
        if fact.product_id in product_nodes:
            graph.add_edge(fact_node.node_id, product_nodes[fact.product_id].node_id, "derived_from", recorded_at=fact.observed_at.isoformat())

    for fact in catalog.facts:
        if fact.supersedes_fact_id and fact.supersedes_fact_id in fact_nodes:
            graph.add_edge(
                fact_nodes[fact.fact_id].node_id,
                fact_nodes[fact.supersedes_fact_id].node_id,
                "supersedes",
                recorded_at=fact.observed_at.isoformat(),
            )

    for verification in catalog.verifications:
        fact_node = fact_nodes.get(verification.fact_id)
        if fact_node is None:
            continue
        verification_node = _add_node(
            graph,
            kind=NodeKind.RESULT,
            source_ref=verification.verification_id,
            version_ref=verification.result,
            recorded_at=verification.checked_at,
            status=verification.result,
            metadata={"verifier": verification.verifier, "source_url": verification.source_url},
        )
        graph.add_edge(fact_node.node_id, verification_node.node_id, "verified_by", recorded_at=verification.checked_at.isoformat())

    evidence_nodes: list[tuple[object, object]] = []
    for record in evidence.records:
        evidence_node = _add_node(
            graph,
            kind=NodeKind.EVIDENCE,
            source_ref=record.evidence_id,
            version_ref=record.state.value,
            recorded_at=datetime.fromisoformat(record.recorded_at),
            status=record.state.value,
            metadata={"location": record.location, "system_type": record.system_type, "source": record.source},
        )
        evidence_nodes.append((record, evidence_node))
        graph.add_edge(evidence_node.node_id, building_node.node_id, "used_by", recorded_at=evidence_node.recorded_at)

    for record, evidence_node in evidence_nodes:
        if record.supersedes:
            target = next((node for item, node in evidence_nodes if item.evidence_id == record.supersedes), None)
            if target is not None:
                graph.add_edge(evidence_node.node_id, target.node_id, "supersedes", recorded_at=evidence_node.recorded_at)

    construction_nodes = []
    for index, assembly in enumerate(load_ledger.assemblies):
        construction_node = _add_node(
            graph,
            kind=NodeKind.CONSTRUCTION,
            source_ref=f"{building.model_id}:assembly:{index}",
            version_ref=version,
            recorded_at=recorded_at,
            metadata={"name": assembly.name, "area_m2": str(assembly.area_m2)},
        )
        construction_nodes.append(construction_node)
        graph.add_edge(building_node.node_id, construction_node.node_id, "derived_from", recorded_at=recorded_at.isoformat())

    load_node = _add_node(
        graph,
        kind=NodeKind.LOAD,
        source_ref=f"load-ledger:{building.model_id}",
        version_ref=version,
        recorded_at=recorded_at,
    )
    graph.add_edge(building_node.node_id, load_node.node_id, "derived_from", recorded_at=recorded_at.isoformat())
    graph.add_edge(environment_node.node_id, load_node.node_id, "derived_from", recorded_at=recorded_at.isoformat())
    for construction_node in construction_nodes:
        graph.add_edge(construction_node.node_id, load_node.node_id, "derived_from", recorded_at=recorded_at.isoformat())
    for _, evidence_node in evidence_nodes:
        graph.add_edge(evidence_node.node_id, load_node.node_id, "used_by", recorded_at=recorded_at.isoformat())

    return graph
