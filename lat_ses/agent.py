from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class LatSesAgent:
    """A minimal conversational agent scaffold for LATSES."""

    name: str = "LATSES-Agent"
    memory: List[str] = field(default_factory=list)

    def remember(self, note: str) -> None:
        """Store an interaction note in memory."""
        self.memory.append(note.strip())

    def respond(self, prompt: str) -> str:
        """Return a simple response to a prompt and remember it."""
        cleaned = (prompt or "").strip()
        if not cleaned:
            self.remember("empty prompt")
            return f"[{self.name}] I can help structure LATSES knowledge and draft responses."

        self.remember(cleaned)
        return f"[{self.name}] I received: {cleaned[:80]}"

    def plan(self, task: str) -> List[str]:
        """Create a simple action plan for a given task."""
        cleaned = (task or "").strip()
        if not cleaned:
            return ["1. Clarify the goal", "2. Draft a response", "3. Review the result"]

        return [
            f"1. Analyze the request: {cleaned}",
            "2. Draft a concise response",
            "3. Review the result for clarity",
        ]
