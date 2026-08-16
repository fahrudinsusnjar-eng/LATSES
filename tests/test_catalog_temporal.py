from datetime import datetime, timezone

from lat_ces.catalog.temporal import (
    FactState,
    ProductIdentity,
    TechnicalFact,
    VerificationRecord,
    evaluate_offer,
)


def t(day: int) -> datetime:
    return datetime(2030, 1, day, tzinfo=timezone.utc)


def test_new_fact_supersedes_old_and_becomes_offerable_only_after_verification() -> None:
    product = ProductIdentity("porotherm-x", "Example", "Ceramic block", "X25")
    old = TechnicalFact(
        "f1", product.product_id, "density", 800, "kg/m3",
        "https://manufacturer.example/old", "old.pdf", t(1), t(1), t(10),
        FactState.SUPERSEDED,
    )
    new = TechnicalFact(
        "f2", product.product_id, "density", 780, "kg/m3",
        "https://manufacturer.example/current", "current.pdf", t(10), t(10), None,
        FactState.CURRENT, "f1",
    )
    before = evaluate_offer(product, (old, new), (), t(12), ("density",))
    assert not before.eligible
    verified = VerificationRecord("v2", "f2", t(11), "independent-loop", new.source_url, "confirmed")
    after = evaluate_offer(product, (old, new), (verified,), t(12), ("density",))
    assert after.eligible
    assert after.current_fact_ids == ("f2",)


def test_unverified_product_never_enters_offer_set() -> None:
    product = ProductIdentity("fan-1", "Example", "Fan", "F1")
    fact = TechnicalFact(
        "f1", product.product_id, "airflow", 250, "m3/h",
        "https://manufacturer.example/f1", "datasheet.pdf", t(1), t(1), None,
        FactState.CURRENT,
    )
    offer = evaluate_offer(product, (fact,), (), t(2), ("airflow",))
    assert not offer.eligible
