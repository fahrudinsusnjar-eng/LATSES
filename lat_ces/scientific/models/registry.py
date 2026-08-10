from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .contract import ScientificModelContract
from .metadata import ScientificModelMetadata


class ModelStatus(str, Enum):
    """Lifecycle status of a scientific model."""

    ACTIVE = "ACTIVE"
    DEPRECATED = "DEPRECATED"


@dataclass(frozen=True)
class ModelRegistryEntry:
    """Immutable registry record for one scientific model."""

    model_id: str
    version: str
    status: ModelStatus
    metadata: ScientificModelMetadata
    contract: ScientificModelContract


class ModelRegistry:
    """Deterministic in-memory registry for scientific models."""

    def __init__(self) -> None:
        self._entries: dict[str, ModelRegistryEntry] = {}

    def register(self, entry: ModelRegistryEntry) -> None:
        """Register a model.

        Existing model identifiers cannot be silently overwritten.
        """

        if not entry.model_id.strip():
            raise ValueError("model_id must not be empty.")

        if not entry.version.strip():
            raise ValueError("version must not be empty.")

        if entry.model_id in self._entries:
            raise ValueError(
                f"Model already registered: '{entry.model_id}'."
            )

        self._entries[entry.model_id] = entry

    def get(self, model_id: str) -> ModelRegistryEntry:
        """Return a registered model entry."""

        try:
            return self._entries[model_id]
        except KeyError as exc:
            raise KeyError(
                f"Model is not registered: '{model_id}'."
            ) from exc

    def has(self, model_id: str) -> bool:
        """Return whether a model is registered."""

        return model_id in self._entries

    def list_models(self) -> tuple[ModelRegistryEntry, ...]:
        """Return registered models in deterministic insertion order."""

        return tuple(self._entries.values())

    def remove(self, model_id: str) -> None:
        """Remove a registered model."""

        try:
            del self._entries[model_id]
        except KeyError as exc:
            raise KeyError(
                f"Model is not registered: '{model_id}'."
            ) from exc
