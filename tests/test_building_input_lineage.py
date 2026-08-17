from datetime import datetime, timezone

from lat_ces.building.model import BuildingModel
from lat_ces.building.environment import SiteEnvironment
from lat_ces.catalog.temporal import FactState, ProductIdentity, TechnicalFact, VerificationRecord
from lat_ces.evidence.historical import HistoricalEvidenceLedger, EvidenceRecord, EvidenceState
from lat_ces.lineage.building_lineage import TechnicalCatalogSnapshot, build_building_input_lineage
from lat_ces.structural.load_ledger import ConstructionAssembly, LoadLedger


def test_building_input_lineage_connects_all_canonical_sources():
    t0 = datetime(2026, 8, 16, tzinfo=timezone.utc)
    building = BuildingModel(name="Test House")
    environment = SiteEnvironment(latitude_deg=44.8, longitude_deg=15.9)
    product = ProductIdentity(product_id="PROD-1", manufacturer="Example", product_family="block", model_code="X25")
    fact = TechnicalFact(
        fact_id="FACT-1",
        product_id="PROD-1",
        property_name="density",
        value=800,
        unit="kg/m3",
        source_url="https://manufacturer.example/x25",
        source_document="x25.pdf",
        observed_at=t0,
        valid_from=t0,
        state=FactState.CURRENT,
    )
    verification = VerificationRecord(
        verification_id="VER-1",
        fact_id="FACT-1",
        checked_at=t0,
        verifier="independent-checker",
        source_url="https://independent.example/check",
        result="confirmed",
    )
    evidence = HistoricalEvidenceLedger()
    evidence.append(EvidenceRecord(
        evidence_id="EVID-1",
        location="44.8,15.9",
        period_start="2010",
        period_end="2025",
        object_type="house",
        system_type="masonry",
        material_or_system="block",
        source="documented survey",
        recorded_at=t0.isoformat(),
        state=EvidenceState.CONFIRMED,
    ))
    ledger = LoadLedger()
    ledger.add(ConstructionAssembly(name="roof", area_m2=120.0)) if False else None

    graph = build_building_input_lineage(
        building,
        TechnicalCatalogSnapshot(products=(product,), facts=(fact,), verifications=(verification,)),
        environment,
        evidence,
        ledger,
        recorded_at=t0,
        version="1",
    )

    kinds = {node.kind.value for node in graph.nodes}
    assert {"building_model", "environment", "product", "fact", "historical_evidence", "load"} <= kinds
    relations = {edge.relation for edge in graph.edges}
    assert {"derived_from", "verified_by", "used_by"} <= relations
    assert graph.validate() == []


def test_technical_fact_supersedes_link_is_order_independent():
    t0 = datetime(2026, 8, 16, tzinfo=timezone.utc)
    t1 = datetime(2030, 1, 1, tzinfo=timezone.utc)
    building = BuildingModel(name="Test House")
    environment = SiteEnvironment(latitude_deg=44.8, longitude_deg=15.9)
    product = ProductIdentity(product_id="PROD-1", manufacturer="Example", product_family="block", model_code="X25")
    old = TechnicalFact(
        fact_id="FACT-OLD", product_id="PROD-1", property_name="density", value=800, unit="kg/m3",
        source_url="https://manufacturer.example/x25", source_document="2026.pdf", observed_at=t0, valid_from=t0,
        state=FactState.SUPERSEDED,
    )
    new = TechnicalFact(
        fact_id="FACT-NEW", product_id="PROD-1", property_name="density", value=780, unit="kg/m3",
        source_url="https://manufacturer.example/x25", source_document="2030.pdf", observed_at=t1, valid_from=t1,
        state=FactState.CURRENT, supersedes_fact_id="FACT-OLD",
    )
    graph = build_building_input_lineage(
        building,
        TechnicalCatalogSnapshot(products=(product,), facts=(new, old)),
        environment,
        HistoricalEvidenceLedger(),
        LoadLedger(),
        recorded_at=t1,
        version="2",
    )
    assert any(edge.relation == "supersedes" for edge in graph.edges)
