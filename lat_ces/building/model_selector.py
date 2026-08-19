"""Canonical BuildingModel selector.

The selector switches only between already constructed canonical
``BuildingModel`` instances. Showcase-only JSON is not converted here.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .model import BuildingModel


@dataclass(frozen=True)
class BuildingModelOption:
    model_id: str
    name: str
    description: str = ""
    source: str = "runtime"


class BuildingModelSelector:
    """Registry and selector for canonical ``BuildingModel`` instances."""

    def __init__(self, model: BuildingModel) -> None:
        self._models = {model.model_id: model}
        self._options = {
            model.model_id: BuildingModelOption(
                model.model_id,
                model.name,
                "Trenutni canonical BuildingModel projekat",
            )
        }
        self._selected_id = model.model_id

    @property
    def selected(self) -> BuildingModel:
        return self._models[self._selected_id]

    @property
    def selected_id(self) -> str:
        return self._selected_id

    def options(self) -> tuple[BuildingModelOption, ...]:
        return tuple(self._options.values())

    def register(
        self,
        model: BuildingModel,
        *,
        description: str = "",
        source: str = "runtime",
    ) -> BuildingModelOption:
        option = BuildingModelOption(model.model_id, model.name, description, source)
        self._models[model.model_id] = model
        self._options[model.model_id] = option
        return option

    def select(self, model_id: str) -> BuildingModel:
        if model_id not in self._models:
            raise KeyError(model_id)
        self._selected_id = model_id
        return self.selected

    def remove(self, model_id: str) -> None:
        if model_id == self._selected_id:
            raise ValueError("Ne može se ukloniti trenutno odabrani BuildingModel")
        if model_id not in self._models:
            raise KeyError(model_id)
        del self._models[model_id]
        del self._options[model_id]

    def __iter__(self) -> Iterable[BuildingModelOption]:
        return iter(self.options())


__all__ = ["BuildingModelOption", "BuildingModelSelector"]
