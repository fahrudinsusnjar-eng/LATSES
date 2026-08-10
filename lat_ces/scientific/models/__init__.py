"""Scientific model metadata and consolidation primitives.

The models package is intentionally additive.

Existing equation classes under
lat_ces.scientific.equations remain the executable calculation layer.
"""

from .metadata import (
    ModelInput,
    ModelOutput,
    ScientificModelMetadata,
)

__all__ = [
    "ModelInput",
    "ModelOutput",
    "ScientificModelMetadata",
]
