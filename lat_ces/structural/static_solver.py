"""Small-strain 2-D truss static solver for the canonical StructuralModel.

BUILDING-006: pure-Python reference solver with no duplicate geometry model.
Inputs are SI: metres, N, and Pa. The solver uses linear elastic axial members.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import hypot

from .model import NodalLoad, StructuralModel


@dataclass(frozen=True)
class TrussResult:
    """Static displacement/result field for a 2-D truss."""

    displacements: dict[str, tuple[float, float]]
    member_axial_forces_n: dict[str, float]


def _solve_linear_system(matrix: list[list[float]], rhs: list[float]) -> list[float]:
    n = len(rhs)
    a = [row[:] + [rhs[i]] for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(a[r][col]))
        if abs(a[pivot][col]) < 1e-12:
            raise ValueError("singular structural stiffness matrix")
        a[col], a[pivot] = a[pivot], a[col]
        scale = a[col][col]
        a[col] = [value / scale for value in a[col]]
        for row in range(n):
            if row == col:
                continue
            factor = a[row][col]
            if factor == 0.0:
                continue
            a[row] = [a[row][j] - factor * a[col][j] for j in range(n + 1)]
    return [a[i][n] for i in range(n)]


def solve_2d_truss(
    structural: StructuralModel,
    material_moduli_pa: dict[str, float],
    load_case: str,
) -> TrussResult:
    """Solve a linear elastic planar truss using the direct stiffness method."""
    findings = structural.validate()
    if findings:
        raise ValueError("invalid structural model: " + "; ".join(findings))
    case = structural.load_cases.get(load_case)
    if case is None:
        raise ValueError(f"unknown load case: {load_case}")
    if not structural.nodes:
        raise ValueError("structural model has no nodes")

    node_ids = list(structural.nodes)
    index = {node_id: 2 * i for i, node_id in enumerate(node_ids)}
    size = 2 * len(node_ids)
    stiffness = [[0.0 for _ in range(size)] for _ in range(size)]
    loads = [0.0] * size

    for load in case.loads:
        base = index[load.node_id]
        loads[base] += load.fx_n
        loads[base + 1] += load.fy_n

    member_cache: list[tuple[str, str, str, float, float, float, float, float]] = []
    for member_id, member in structural.members.items():
        if member.start_node_id not in structural.nodes or member.end_node_id not in structural.nodes:
            raise ValueError(f"member {member_id} references an unknown node")
        if member.material_id is None:
            raise ValueError(f"member {member_id} requires material_id for static solve")
        if member.material_id not in material_moduli_pa:
            raise ValueError(f"missing Young's modulus for material {member.material_id}")
        start = structural.nodes[member.start_node_id]
        end = structural.nodes[member.end_node_id]
        dx = end.x - start.x
        dy = end.y - start.y
        length = hypot(dx, dy)
        if length <= 0:
            raise ValueError(f"member {member_id} has zero length")
        c = dx / length
        s = dy / length
        e = material_moduli_pa[member.material_id]
        if e <= 0 or member.area_m2 <= 0:
            raise ValueError(f"member {member_id} has invalid stiffness properties")
        k = e * member.area_m2 / length
        i = index[member.start_node_id]
        j = index[member.end_node_id]
        local = (
            k * c * c,
            k * c * s,
            k * s * s,
            k,
        )
        stiffness[i][i] += local[0]
        stiffness[i][i + 1] += local[1]
        stiffness[i + 1][i] += local[1]
        stiffness[i + 1][i + 1] += local[2]
        stiffness[j][j] += local[0]
        stiffness[j][j + 1] += local[1]
        stiffness[j + 1][j] += local[1]
        stiffness[j + 1][j + 1] += local[2]
        stiffness[i][j] -= local[0]
        stiffness[i][j + 1] -= local[1]
        stiffness[i + 1][j] -= local[1]
        stiffness[i + 1][j + 1] -= local[2]
        stiffness[j][i] -= local[0]
        stiffness[j][i + 1] -= local[1]
        stiffness[j + 1][i] -= local[1]
        stiffness[j + 1][i + 1] -= local[2]
        member_cache.append((member_id, member.start_node_id, member.end_node_id, length, c, s, e, member.area_m2))

    for support in structural.supports.values():
        base = index[support.node_id]
        if support.restraints[0]:
            stiffness[base] = [0.0] * size
            for r in range(size):
                stiffness[r][base] = 0.0
            stiffness[base][base] = 1.0
            loads[base] = 0.0
        if support.restraints[1]:
            dof = base + 1
            stiffness[dof] = [0.0] * size
            for r in range(size):
                stiffness[r][dof] = 0.0
            stiffness[dof][dof] = 1.0
            loads[dof] = 0.0

    solved = _solve_linear_system(stiffness, loads)
    displacements = {
        node_id: (solved[index[node_id]], solved[index[node_id] + 1]) for node_id in node_ids
    }

    axial_forces: dict[str, float] = {}
    for member_id, start_id, end_id, length, c, s, e, area in member_cache:
        ux, uy = displacements[start_id]
        vx, vy = displacements[end_id]
        extension = (vx - ux) * c + (vy - uy) * s
        axial_forces[member_id] = e * area * extension / length

    return TrussResult(displacements, axial_forces)


def nodal_load(case: str, node_id: str, fx_n: float = 0.0, fy_n: float = 0.0) -> NodalLoad:
    """Convenience constructor used by integrations and GUI adapters."""
    return NodalLoad(node_id=node_id, fx_n=fx_n, fy_n=fy_n)
