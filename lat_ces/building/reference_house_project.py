"""Editable reference-house project adapter.

The adapter imports the existing reference-house specification into the canonical
BuildingWorkflow as one project with independently selectable levels. Room area
and room metadata are preserved in both BuildingProjectSpec and the canonical
BuildingModel; room topology remains a deterministic placeholder until drafting
replaces it with user-authored geometry.
"""
from __future__ import annotations

from math import sqrt

from lat_ces.reference_house import ReferenceHouse
from .geometry import Box3D, Point3D
from .model import BuildingModel, Level, Material, Roof, Room
from .orientation import BuildingOrientation
from .project_spec import (
    BuildingProjectSpec,
    JoinerySpec,
    LevelProjectSpec,
    RoomSpec,
    WallConstructionSpec,
)
from .workflow import BuildingWorkflow, make_envelope_floor_plan


def _room_spec(room: dict) -> RoomSpec:
    area = max(0.01, float(room.get("area_m2", 0.0)))
    # Preserve exact area while leaving the aspect ratio explicitly provisional.
    length = sqrt(area)
    width = area / length
    return RoomSpec(
        name=str(room.get("name", "Prostorija")),
        length_m=length,
        width_m=width,
        role=str(room.get("orientation", "room")),
    )


def _add_reference_rooms(level: Level, room_data: list[dict]) -> None:
    """Materialize reference-room area/volume into the canonical BuildingModel.

    The reference-house source intentionally does not contain drafted wall topology.
    Until the drafting layer supplies that topology, rooms are represented as
    deterministic non-overlapping strips spanning the level length. Their footprint
    area and height exactly match the reference data, so downstream performance
    models can use real BuildingModel room identities without inventing dimensions.
    """
    y = 0.0
    for data in room_data:
        height = float(data.get("height_m", level.height))
        area = float(data.get("area_m2", 0.0))
        if height <= 0.0 or area <= 0.0:
            continue
        length = level.length_m
        width = area / length
        if y + width > level.width_m + 1e-9:
            raise ValueError(
                f"Reference room areas exceed level envelope for {level.name}: "
                f"{y + width:.6g} m > {level.width_m:.6g} m"
            )
        level.add_room(
            Room(
                name=str(data.get("name", "Prostorija")),
                footprint=Box3D(
                    origin=Point3D(0.0, y, level.elevation),
                    length=length,
                    width=width,
                    height=height,
                ),
            )
        )
        y += width


def build_reference_house_workflow() -> BuildingWorkflow:
    house = ReferenceHouse.default()
    data = house.data
    dimensions = data["dimensions"]
    orientation = BuildingOrientation()
    model = BuildingModel(name=str(data["name"]), model_id=str(data["model_id"]), orientation=orientation)

    envelope = data.get("envelope", {})
    wall = envelope.get("exterior_wall", {})
    wall_construction = WallConstructionSpec(
        block_brand=str(wall.get("masonry_block", "")),
        wall_thickness_m=0.25,
        insulation_type=str(wall.get("insulation", "")),
        insulation_thickness_m=float(wall.get("insulation_thickness_m", 0.0)),
        exterior_cladding=str(wall.get("facade_finish", "")),
        interior_cladding=str(wall.get("interior_finish", "")),
        render_thickness_m=float(wall.get("interior_finish_thickness_m", 0.0)),
    )

    project = BuildingProjectSpec(
        name=str(data["name"]),
        floor_count=len(data["levels"]),
        floor_count_finalized=True,
        roof_shape=str(data["roof"]["type"]),
        roof_height_m=0.0,
        orientation=orientation,
    )
    project.roof.roof_type = str(data["roof"]["type"])
    project.roof.length_m = float(dimensions["length_m"])
    project.roof.width_m = float(dimensions["width_m"])
    project.roof.slope_deg = float(data["roof"].get("slope_deg", 0.0))
    project.roof.covering = str(data["roof"].get("covering", ""))
    project.roof.construction = "Drvena krovna građa"
    project.roof.height_m = 0.0

    for level_data in data["levels"]:
        rooms = [_room_spec(room) for room in level_data.get("rooms", [])]
        joinery = data.get("joinery", {})
        level_spec = LevelProjectSpec(
            name=str(level_data["name"]),
            height_m=float(dimensions["level_height_m"]),
            length_m=float(dimensions["length_m"]),
            width_m=float(dimensions["width_m"]),
            construction=wall_construction,
            cladding=str(wall.get("facade_finish", "")),
            joinery=JoinerySpec(
                material=str(joinery.get("default_frame", "")),
                glazing="3 stakla / argon / Low-E / warm edge",
                frame_type=str(joinery.get("default_frame", "")),
                thermal_transmittance_w_m2k=0.7,
                opening_count=0,
            ),
            rooms=rooms,
            finalized=False,
        )
        project.levels.append(level_spec)

    workflow = BuildingWorkflow(model=model, project_spec=project, current_step=3)
    previous = None
    for level_data in data["levels"]:
        level = model.add_level(
            Level(
                name=str(level_data["name"]),
                elevation=0.0 if previous is None else previous.top_elevation,
                height=float(dimensions["level_height_m"]),
                length_m=float(dimensions["length_m"]),
                width_m=float(dimensions["width_m"]),
                wall_construction=str(wall.get("masonry_block", "")),
                insulation=str(wall.get("insulation", "")),
                cladding=str(wall.get("facade_finish", "")),
                joinery=str(joinery.get("default_frame", "")),
                facade_finish=str(wall.get("facade_finish", "")),
                insulation_material=str(wall.get("insulation", "")),
                insulation_thickness_m=float(wall.get("insulation_thickness_m", 0.0)),
                interior_plaster_material=str(wall.get("interior_finish", "")),
                interior_plaster_thickness_m=float(wall.get("interior_finish_thickness_m", 0.0)),
                dead_load_kpa=float(level_data.get("loads", {}).get("dead_kpa", 0.0)),
                live_load_kpa=float(level_data.get("loads", {}).get("live_kpa", 0.0)),
            )
        )
        level.set_floor_plan(make_envelope_floor_plan(level.name, level.length_m, level.width_m, 0.25))
        _add_reference_rooms(level, level_data.get("rooms", []))
        previous = level

    roof_data = data["roof"]
    model.set_roof(
        Roof(
            roof_type=str(roof_data["type"]),
            construction="Drvena krovna građa",
            covering=str(roof_data.get("covering", "")),
            substructure=f"Rog {roof_data.get('rafter_section_mm', [100, 200])[0]}×{roof_data.get('rafter_section_mm', [100, 200])[1]} mm",
            support=str(roof_data.get("ridge_direction", "")),
            length_m=float(dimensions["length_m"]),
            width_m=float(dimensions["width_m"]),
            slope_deg=float(roof_data.get("slope_deg", 0.0)),
            height_m=0.0,
        )
    )
    workflow.active_level_id = next(iter(model.levels), None)
    return workflow


__all__ = ["build_reference_house_workflow"]
