"""Solver-neutral structural model attached to the canonical BuildingModel.

BUILDING-004: structural topology references the shared building model rather
than duplicating geometry. Values at this boundary use SI units: metres, N,
and N·m.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from lat_ces.building.model import BuildingModel


@dataclass(frozen=True)
class StructuralNode:
    """Structural analysis node in global Cartesian coordinates."""

    node_id: str
    x: float
    y: float
    z: float
    element_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class StructuralMember:
    """Two-node structural member referencing a building element when known."""

    member_id: str
    start_node_id: str
    end_node_id: str
    element_id: str | None = None
    material_id: str | None = None
    area_m2: float = 0.0
    inertia_m4: float | None = None

    def __post_init__(self) -> None:
        if not self.member_id:
            raise ValueError("member_id must not be empty")
        if self.start_node_id == self.end_node_id:
            raise ValueError("structural member cannot connect a node to itself")
        if self.area_m2 <= 0:
            raise ValueError("member area must be > 0")
        if self.inertia_m4 is not None and self.inertia_m4 <= 0:
            raise ValueError("member inertia must be > 0")


@dataclass(frozen=True)
class SupportCondition:
    """Boolean translational/rotational restraints (UX, UY, UZ, RX, RY, RZ)."""

    node_id: str
    restraints: tuple[bool, bool, bool, bool, bool, bool]

    def __post_init__(self) -> None:
        if len(self.restraints) != 6:
            raise ValueError("support restraints must contain 6 boolean values")
        if not all(isinstance(value, bool) for value in self.restraints):
            raise TypeError("support restraints must be boolean")


@dataclass(frozen=True)
class NodalLoad:
    """Concentrated load in global coordinates: Fx,Fy,Fz,Mx,My,Mz."""

    node_id: str
    fx_n: float = 0.0
    fy_n: float = 0.0
    fz_n: float = 0.0
    mx_nm: float = 0.0
    my_nm: float = 0.0
    mz_nm: float = 0.0


@dataclass
class LoadCase:
    """Named set of nodal loads."""

    name: str
    loads: list[NodalLoad] = field(default_factory=list)

    def add_load(self, load: NodalLoad) -> NodalLoad:
        self.loads.append(load)
        return load


@dataclass
class StructuralModel:
    """Structural domain model that references one canonical BuildingModel."""

    building: BuildingModel
    nodes: dict[str, StructuralNode] = field(default_factory=dict)
    members: dict[str, StructuralMember] = field(default_factory=dict)
    supports: dict[str, SupportCondition] = field(default_factory=dict)
    load_cases: dict[str, LoadCase] = field(default_factory=dict)

    def add_node(self, node: StructuralNode) -> StructuralNode:
        if node.node_id in self.nodes:
            raise ValueError(f"Duplicate structural node id: {node.node_id}")
        self.nodes[node.node_id] = node
        return node

    def add_member(self, member: StructuralMember) -> StructuralMember:
        if member.member_id in self.members:
            raise ValueError(f"Duplicate structural member id: {member.member_id}")
        self.members[member.member_id] = member
        return member

    def add_support(self, support: SupportCondition) -> SupportCondition:
        if support.node_id in self.supports:
            raise ValueError(f"Duplicate support for node: {support.node_id}")
        self.supports[support.node_id] = support
        return support

    def add_load_case(self, case: LoadCase) -> LoadCase:
        if not case.name.strip():
            raise ValueError("LoadCase.name must not be empty")
        if case.name in self.load_cases:
            raise ValueError(f"Duplicate load case: {case.name}")
        self.load_cases[case.name] = case
        return case

    def validate(self) -> list[str]:
        """Return reference/topology findings without running a solver."""
        findings: list[str] = []
        element_ids = {element.element_id for element in self.building.all_elements()}
        material_ids = set(self.building.materials)

        for member in self.members.values():
            if member.start_node_id not in self.nodes:
                findings.append(f"Missing start node: {member.start_node_id}")
            if member.end_node_id not in self.nodes:
                findings.append(f"Missing end node: {member.end_node_id}")
            if member.element_id is not None and member.element_id not in element_ids:
                findings.append(f"Unknown building element: {member.element_id}")
            if member.material_id is not None and member.material_id not in material_ids:
                findings.append(f"Unknown material: {member.material_id}")

        for support in self.supports.values():
            if support.node_id not in self.nodes:
                findings.append(f"Missing support node: {support.node_id}")

        for case in self.load_cases.values():
            for load in case.loads:
                if load.node_id not in self.nodes:
                    findings.append(f"Missing load node: {load.node_id}")

        return findings
