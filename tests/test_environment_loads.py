from lat_ces.building.environment import EnvironmentalFact, SiteEnvironment, SiteVerificationGate, VerificationState
from lat_ces.structural.environment_loads import build_environmental_load_snapshot, apply_environmental_actions
from lat_ces.structural.load_ledger import LoadLedger


def _verified_site() -> SiteEnvironment:
    site = SiteEnvironment(latitude_deg=44.8, longitude_deg=15.9)
    for key in SiteVerificationGate().required_keys:
        site.add_fact(EnvironmentalFact(
            key=key,
            value=1.0,
            unit="SI",
            source_url="https://official.example/source",
            source_name="Official source",
            observation_date="2026-01-01",
            retrieval_date="2026-08-16",
            verification_state=VerificationState.VERIFIED,
            verifier="independent-checker",
            verification_date="2026-08-16",
            verification_source_url="https://independent.example/check",
        ))
    return site


def test_unverified_site_cannot_feed_structural_environmental_loads():
    site = SiteEnvironment(latitude_deg=44.8, longitude_deg=15.9)
    try:
        build_environmental_load_snapshot(site)
    except ValueError:
        return
    raise AssertionError("unverified environmental data must not enter structural loads")


def test_verified_site_produces_snapshot_without_mutating_history():
    site = _verified_site()
    before = tuple(site.facts)
    snapshot = build_environmental_load_snapshot(site)
    assert snapshot.snow_ground_characteristic == 1.0
    assert tuple(site.facts) == before


def test_load_ledger_adapter_is_read_only_boundary():
    site = _verified_site()
    ledger = LoadLedger()
    snapshot = apply_environmental_actions(site, ledger)
    assert snapshot.wind_basic_velocity == 1.0
    assert len(site.facts) == len(SiteVerificationGate().required_keys)
    assert ledger.entries == []
