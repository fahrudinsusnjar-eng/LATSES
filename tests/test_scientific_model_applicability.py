from lat_ces.scientific.models import (
    ApplicabilityEvaluator,
    ApplicabilityReason,
    ApplicabilityRequest,
    ApplicabilityStatus,
    ModelInput,
    ModelOutput,
    ModelRegistry,
    ModelRegistryEntry,
    ModelStatus,
    ScientificModelContract,
    ScientificModelMetadata,
)
from lat_ces.scientific.dimensions.dimension import DIMENSIONLESS


def make_registry() -> ModelRegistry:
    metadata = ScientificModelMetadata(
        model_id="TEST-001",
        name="Test Model",
        domain="testing",
        description="Test scientific model.",
        equation="y = x",
        inputs=(
            ModelInput(
                name="x",
                description="Test input.",
                dimension=DIMENSIONLESS,
                required=True,
            ),
        ),
        outputs=(
            ModelOutput(
                name="y",
                description="Test output.",
                dimension=DIMENSIONLESS,
            ),
        ),
    )

    contract = ScientificModelContract(metadata)

    registry = ModelRegistry()

    registry.register(
        ModelRegistryEntry(
            model_id="TEST-001",
            version="1.0",
            status=ModelStatus.ACTIVE,
            metadata=metadata,
            contract=contract,
        )
    )

    return registry


def test_unregistered_model_is_rejected() -> None:
    evaluator = ApplicabilityEvaluator(make_registry())

    result = evaluator.evaluate(
        ApplicabilityRequest(model_id="UNKNOWN")
    )

    assert result.status is ApplicabilityStatus.MODEL_UNAVAILABLE
    assert result.applicable is False
    assert result.reason_code is ApplicabilityReason.MODEL_NOT_REGISTERED


def test_missing_context_does_not_produce_result() -> None:
    evaluator = ApplicabilityEvaluator(make_registry())

    result = evaluator.evaluate(
        ApplicabilityRequest(
            model_id="TEST-001",
            inputs={"x": 1},
        )
    )

    assert result.status is ApplicabilityStatus.INSUFFICIENT_EVIDENCE
    assert result.applicable is False
    assert result.reason_code is ApplicabilityReason.CONTEXT_MISSING


def test_empty_context_is_insufficient() -> None:
    evaluator = ApplicabilityEvaluator(make_registry())

    result = evaluator.evaluate(
        ApplicabilityRequest(
            model_id="TEST-001",
            context={},
            inputs={"x": 1},
        )
    )

    assert result.status is ApplicabilityStatus.INSUFFICIENT_EVIDENCE
    assert result.reason_code is ApplicabilityReason.CONTEXT_INCOMPLETE


def test_valid_context_is_applicable() -> None:
    evaluator = ApplicabilityEvaluator(make_registry())

    result = evaluator.evaluate(
        ApplicabilityRequest(
            model_id="TEST-001",
            context={"entity": "test"},
            inputs={"x": 1},
        )
    )

    assert result.status is ApplicabilityStatus.APPLICABLE
    assert result.applicable is True
    assert result.reason_code is ApplicabilityReason.APPLICABLE_INPUTS_VALID


def test_deprecated_model_is_superseded() -> None:
    registry = make_registry()
    entry = registry.get("TEST-001")

    registry.remove("TEST-001")

    registry.register(
        ModelRegistryEntry(
            model_id=entry.model_id,
            version=entry.version,
            status=ModelStatus.DEPRECATED,
            metadata=entry.metadata,
            contract=entry.contract,
        )
    )

    evaluator = ApplicabilityEvaluator(registry)

    result = evaluator.evaluate(
        ApplicabilityRequest(
            model_id="TEST-001",
            context={"entity": "test"},
            inputs={"x": 1},
        )
    )

    assert result.status is ApplicabilityStatus.MODEL_SUPERSEDED
    assert result.applicable is False
    assert result.reason_code is ApplicabilityReason.MODEL_SUPERSEDED


def test_wrong_version_is_rejected() -> None:
    evaluator = ApplicabilityEvaluator(make_registry())

    result = evaluator.evaluate(
        ApplicabilityRequest(
            model_id="TEST-001",
            model_version="9.0",
            context={"entity": "test"},
            inputs={"x": 1},
        )
    )

    assert result.status is ApplicabilityStatus.MODEL_UNAVAILABLE
    assert result.reason_code is ApplicabilityReason.MODEL_VERSION_UNAVAILABLE
def test_missing_required_input_is_rejected() -> None:
    evaluator = ApplicabilityEvaluator(make_registry())

    result = evaluator.evaluate(
        ApplicabilityRequest(
            model_id="TEST-001",
            context={"entity": "test"},
            inputs={},
        )
    )

    assert result.status is ApplicabilityStatus.INVALID_INPUT
    assert result.applicable is False
    assert result.reason_code is ApplicabilityReason.REQUIRED_INPUT_MISSING
    assert result.violations == ("x",)


def test_invalid_contract_blocks_applicability() -> None:
    registry = make_registry()
    entry = registry.get("TEST-001")

    invalid_metadata = ScientificModelMetadata(
        model_id=entry.metadata.model_id,
        name=entry.metadata.name,
        domain=entry.metadata.domain,
        description=entry.metadata.description,
        equation=entry.metadata.equation,
        inputs=(
            entry.metadata.inputs[0],
            ModelInput(
                name="x",
                description="Duplicate input.",
                dimension=DIMENSIONLESS,
                required=True,
            ),
        ),
        outputs=entry.metadata.outputs,
    )

    invalid_entry = ModelRegistryEntry(
        model_id=entry.model_id,
        version=entry.version,
        status=ModelStatus.ACTIVE,
        metadata=invalid_metadata,
        contract=ScientificModelContract(invalid_metadata),
    )

    registry.remove("TEST-001")
    registry.register(invalid_entry)

    evaluator = ApplicabilityEvaluator(registry)

    result = evaluator.evaluate(
        ApplicabilityRequest(
            model_id="TEST-001",
            context={"entity": "test"},
            inputs={"x": 1},
        )
    )

    assert result.status is ApplicabilityStatus.CONTRACT_INVALID
    assert result.applicable is False
    assert result.reason_code is ApplicabilityReason.CONTRACT_VIOLATION
    assert result.violations == (
        "DUPLICATE_INPUT: Duplicate input name: 'x'.",
    )
