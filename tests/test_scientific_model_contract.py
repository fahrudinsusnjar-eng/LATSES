import pytest

from lat_ces.scientific.dimensions.dimension import (
    DIMENSIONLESS,
    LENGTH,
)
from lat_ces.scientific.models import (
    ModelInput,
    ModelOutput,
    ScientificModelContract,
    ScientificModelMetadata,
)


def make_metadata(
    *,
    inputs=None,
    outputs=None,
):
    return ScientificModelMetadata(
        model_id="SMC-TEST",
        name="Contract Test Model",
        domain="Testing",
        description="Test scientific model contract.",
        equation="y = x",
        inputs=(
            ModelInput(
                name="x",
                description="Input value.",
                dimension=LENGTH,
            ),
        )
        if inputs is None
        else inputs,
        outputs=(
            ModelOutput(
                name="y",
                description="Output value.",
                dimension=DIMENSIONLESS,
            ),
        )
        if outputs is None
        else outputs,
    )


def test_valid_contract():
    contract = ScientificModelContract(make_metadata())

    assert contract.validate() == ()
    assert contract.is_valid is True


def test_duplicate_input_names_are_rejected():
    metadata = make_metadata(
        inputs=(
            ModelInput(
                name="x",
                description="First input.",
                dimension=LENGTH,
            ),
            ModelInput(
                name="x",
                description="Second input.",
                dimension=LENGTH,
            ),
        )
    )

    contract = ScientificModelContract(metadata)

    issues = contract.validate_inputs()

    assert any(issue.code == "DUPLICATE_INPUT" for issue in issues)
    assert contract.is_valid is False


def test_duplicate_output_names_are_rejected():
    metadata = make_metadata(
        outputs=(
            ModelOutput(
                name="y",
                description="First output.",
                dimension=DIMENSIONLESS,
            ),
            ModelOutput(
                name="y",
                description="Second output.",
                dimension=DIMENSIONLESS,
            ),
        )
    )

    contract = ScientificModelContract(metadata)

    issues = contract.validate_outputs()

    assert any(issue.code == "DUPLICATE_OUTPUT" for issue in issues)
    assert contract.is_valid is False


def test_empty_input_name_is_rejected():
    metadata = make_metadata(
        inputs=(
            ModelInput(
                name="",
                description="Input value.",
                dimension=LENGTH,
            ),
        )
    )

    issues = ScientificModelContract(metadata).validate_inputs()

    assert any(issue.code == "EMPTY_INPUT_NAME" for issue in issues)


def test_empty_output_name_is_rejected():
    metadata = make_metadata(
        outputs=(
            ModelOutput(
                name="",
                description="Output value.",
                dimension=DIMENSIONLESS,
            ),
        )
    )

    issues = ScientificModelContract(metadata).validate_outputs()

    assert any(issue.code == "EMPTY_OUTPUT_NAME" for issue in issues)


def test_empty_input_description_is_rejected():
    metadata = make_metadata(
        inputs=(
            ModelInput(
                name="x",
                description="",
                dimension=LENGTH,
            ),
        )
    )

    issues = ScientificModelContract(metadata).validate_inputs()

    assert any(
        issue.code == "EMPTY_INPUT_DESCRIPTION"
        for issue in issues
    )


def test_empty_output_description_is_rejected():
    metadata = make_metadata(
        outputs=(
            ModelOutput(
                name="y",
                description="",
                dimension=DIMENSIONLESS,
            ),
        )
    )

    issues = ScientificModelContract(metadata).validate_outputs()

    assert any(
        issue.code == "EMPTY_OUTPUT_DESCRIPTION"
        for issue in issues
    )


def test_contract_checks_dimensions():
    metadata = make_metadata()

    contract = ScientificModelContract(metadata)

    assert contract.validate_dimensions() == ()


def test_validation_is_deterministic():
    metadata = make_metadata(
        inputs=(
            ModelInput(
                name="x",
                description="",
                dimension=LENGTH,
            ),
            ModelInput(
                name="x",
                description="",
                dimension=LENGTH,
            ),
        )
    )

    contract = ScientificModelContract(metadata)

    first = contract.validate()
    second = contract.validate()

    assert first == second
