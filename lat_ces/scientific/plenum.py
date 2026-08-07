"""Backward-compatible import for scientific plenum analysis."""

from lat_ces.scientific.analysis.plenum import (
    PlenumAnalysisEngine,
    SafetyReport,
    SafetyStatus,
)

__all__ = ["SafetyStatus", "SafetyReport", "PlenumAnalysisEngine"]