from lat_ces.building.environment import EnvironmentalFact, SiteEnvironment, SiteVerificationGate, VerificationState


def _fact(key: str) -> EnvironmentalFact:
    return EnvironmentalFact(
        key=key,
        value=1.0,
        unit="kN/m2",
        source_url="https://official.example/source",
        source_name="Official source",
        observation_date="2026-01-01",
        retrieval_date="2026-08-16",
        verification_state=VerificationState.VERIFIED,
        verifier="independent-checker",
        verification_date="2026-08-16",
        verification_source_url="https://independent.example/check",
    )


def test_unverified_site_facts_block_climatic_structural_analysis():
    site = SiteEnvironment(latitude_deg=44.8, longitude_deg=15.9)
    gate = SiteVerificationGate()
    assert not gate.ready_for_climatic_structural_analysis(site)


def test_all_verified_site_facts_open_climatic_structural_gate():
    site = SiteEnvironment(latitude_deg=44.8, longitude_deg=15.9)
    for key in gate_keys := SiteVerificationGate().required_keys:
        site.add_fact(_fact(key))
    assert SiteVerificationGate(gate_keys).ready_for_climatic_structural_analysis(site)
