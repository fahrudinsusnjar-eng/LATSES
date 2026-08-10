import pytest

from lat_ces.scientific.dimensions.dimension import (
    DIMENSIONLESS,
    LENGTH,
    MASS,
    TIME,
)
from lat_ces.scientific.models import (
    ModelInput,
    ModelOutput,
    ScientificModelMetadata,
)


def test_scientific_model_metadata_creation():
    metadata = ScientificModelMetadata(
        model_id="SMN-001",
        name="Reynolds Number",
        domain="Fluid Mechanics",
        description="Dimensionless flow-regime indicator.",
        equation="Re = rho * v * L / mu",
        inputs=(
            ModelInput(
                name="density",
                description="Fluid density.",
                dimension=MASS / (LENGTH**3),
            ),
            ModelInput(
                name="velocity",
                description="Characteristic fluid velocity.",
                dimension=LENGTH / TIME,
            ),
        ),
        outputs=(
            ModelOutput(
                name="reynolds_number",
                description="Dimensionless Reynolds number.",
                dimension=DIMENSIONLESS,
            ),
        ),
        assumptions=(
            "Continuum fluid model.",
            "Constant properties over the evaluated state.",
        ),
        validity=(
            "Validity depends on the physical flow configuration.",
        ),
        references=(
            "Standard fluid-mechanics definition of Reynolds number.",
        ),
        equation_class="ReynoldsNumberEquation",
    )

    assert metadata.model_id == "SMN-001"
    assert metadata.name == "Reynolds Number"
    assert metadata.domain == "Fluid Mechanics"
    assert metadata.equation == "Re = rho * v * L / mu"

    assert metadata.input_names == (
        "density",
        "velocity",
    )

    assert metadata.output_names == (
        "reynolds_number",
    )

    assert metadata.equation_class == "ReynoldsNumberEquation"


def test_metadata_is_immutable():
    metadata = ScientificModelMetadata(
        model_id="SMN-TEST",
        name="Test Model",
        domain="Testing",
        description="Metadata test.",
        equation="y = x",
        inputs=(
            ModelInput(
                name="x",
                description="Input.",
                dimension=DIMENSIONLESS,
            ),
        ),
        outputs=(
            ModelOutput(
                name="y",
                description="Output.",
                dimension=DIMENSIONLESS,
            ),
        ),
    )

    with pytest.raises(AttributeError):
        metadata.name = "Changed"


def test_model_input_can_be_optional():
    item = ModelInput(
        name="reference_temperature",
        description="Optional reference temperature.",
        dimension=DIMENSIONLESS,
        required=False,
    )

    assert item.name == "reference_temperature"
    assert item.required is False


def test_model_metadata_requires_identity():
    with pytest.raises(ValueError):
        ScientificModelMetadata(
            model_id="",
            name="Test",
            domain="Testing",
            description="Description",
            equation="y = x",
            inputs=(
                ModelInput(
                    name="x",
                    description="Input.",
                    dimension=DIMENSIONLESS,
                ),
            ),
            outputs=(
                ModelOutput(
                    name="y",
                    description="Output.",
                    dimension=DIMENSIONLESS,
                ),
            ),
        )


def test_model_metadata_requires_inputs():
    with pytest.raises(ValueError):
        ScientificModelMetadata(
            model_id="SMN-TEST",
            name="Test",
            domain="Testing",
            description="Description",
            equation="y = x",
            inputs=(),
            outputs=(
                ModelOutput(
                    name="y",
                    description="Output.",
                    dimension=DIMENSIONLESS,
                ),
            ),
        )


def test_model_metadata_requires_outputs():
    with pytest.raises(ValueError):
        ScientificModelMetadata(
            model_id="SMN-TEST",
            name="Test",
            domain="Testing",
            description="Description",
            equation="y = x",
            inputs=(
                ModelInput(
                    name="x",
                    description="Input.",
                    dimension=DIMENSIONLESS,
                ),
            ),
            outputs=(),
        )
