"""Canonical solver-neutral structural domain for LAT-CES."""

from .model import (
    LoadCase,
    NodalLoad,
    StructuralMember,
    StructuralModel,
    StructuralNode,
    SupportCondition,
)
from .roof import RoofLayer, RoofLoadModel, RoofLoadResult, RoofSpec

__all__ = [
    "StructuralModel",
    "StructuralNode",
    "StructuralMember",
    "SupportCondition",
    "NodalLoad",
    "LoadCase",
    "RoofLayer",
    "RoofSpec",
    "RoofLoadModel",
    "RoofLoadResult",
]
