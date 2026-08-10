import pytest

from lat_ces.scientific.dimensions.dimension import (
    DIMENSIONLESS,
    LENGTH,
)
from lat_ces.scientific.models import (
    ModelInput,
    ModelOutput,
    ModelRegistry,
    ModelRegistryEntry,
    ModelStatus,
    ScientificModelContract,
    ScientificModelMetadata,
)


def make_entry(
    model_id: str = "test_model",
    version: str = "1.0",
    status: ModelStatus = ModelStatus.ACTIVE,
) -> ModelRegistryEntry:
    metadata = ScientificModelMetadata(
        model_id=model_id,
        name="Test Model",
        domain="Testing",
        description="Registry test model.",
        equation="y = x",
        inputs=(
            ModelInput(
                name="x",
                description="Input value.",
                dimension=LENGTH,
            ),
        ),
        outputs=(
            ModelOutput(
                name="y",
                description="Output value.",
                dimension=DIMENSIONLESS,
            ),
        ),
    )

    contract = ScientificModelContract(metadata)

    return ModelRegistryEntry(
        model_id=model_id,
        version=version,
        status=status,
        metadata=metadata,
        contract=contract,
    )


def test_register_and_get_model():
    registry = ModelRegistry()
    entry = make_entry()

    registry.register(entry)

    assert registry.has("test_model")
    assert registry.get("test_model") == entry


def test_duplicate_model_id_is_rejected():
    registry = ModelRegistry()

    registry.register(make_entry())

    with pytest.raises(ValueError, match="already registered"):
        registry.register(make_entry())


def test_missing_model_is_rejected():
    registry = ModelRegistry()

    with pytest.raises(KeyError, match="not registered"):
        registry.get("missing_model")


def test_has_returns_false_for_missing_model():
    registry = ModelRegistry()

    assert registry.has("missing_model") is False


def test_list_models_is_deterministic():
    registry = ModelRegistry()

    first = make_entry("first")
    second = make_entry("second")

    registry.register(first)
    registry.register(second)

    assert registry.list_models() == (first, second)


def test_version_is_preserved():
    registry = ModelRegistry()
    entry = make_entry(version="2.3")

    registry.register(entry)

    assert registry.get("test_model").version == "2.3"


def test_status_is_preserved():
    registry = ModelRegistry()
    entry = make_entry(status=ModelStatus.DEPRECATED)

    registry.register(entry)

    assert (
        registry.get("test_model").status
        is ModelStatus.DEPRECATED
    )


def test_empty_model_id_is_rejected():
    registry = ModelRegistry()

    with pytest.raises(ValueError, match="model_id"):
        registry.register(make_entry(model_id=""))


def test_empty_version_is_rejected():
    registry = ModelRegistry()

    with pytest.raises(ValueError, match="version"):
        registry.register(make_entry(version=""))


def test_remove_model():
    registry = ModelRegistry()
    registry.register(make_entry())

    registry.remove("test_model")

    assert registry.has("test_model") is False


def test_remove_missing_model_is_rejected():
    registry = ModelRegistry()

    with pytest.raises(KeyError, match="not registered"):
        registry.remove("missing_model")
