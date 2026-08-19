"""Small reference house used as an integration model for LATCES.

The example is intentionally small and deterministic: one 10 x 8 m level,
2.80 m storey height, four rooms, real walls/openings, and material data.
It is a seed model for connecting one geometry to downstream engineering.
"""
from .core import BuildingModel, Level, Material, Opening, Room, Wall


def make_small_reference_house() -> BuildingModel:
    """Return a compact, fully populated BuildingModel reference case."""
    brick = Material("brick", density_kg_m3=1800.0, conductivity_w_mk=0.72)
    concrete = Material("reinforced concrete", density_kg_m3=2400.0, conductivity_w_mk=2.30)
    building = BuildingModel(name="LATCES Small Reference House")
    building.materials[brick.name] = brick
    building.materials[concrete.name] = concrete

    level = Level("L0", "Ground floor", 10.0, 8.0, 2.80)
    level.add_room(Room("R1", "Living", 5.0, 4.0, 2.80))
    level.add_room(Room("R2", "Kitchen", 5.0, 4.0, 2.80))
    level.add_room(Room("R3", "Bedroom", 5.0, 4.0, 2.80))
    level.add_room(Room("R4", "Service", 5.0, 4.0, 2.80))

    # Exterior walls: 20 cm brick, 2.80 m high.
    south = Wall("W-S", 10.0, 0.20, 2.80, brick)
    south.add_opening(Opening("door", 0.90, 2.10, position_m=1.20))
    south.add_opening(Opening("window", 1.50, 1.20, sill_height_m=0.90, position_m=5.00))
    north = Wall("W-N", 10.0, 0.20, 2.80, brick)
    north.add_opening(Opening("window", 1.50, 1.20, sill_height_m=0.90, position_m=3.00))
    east = Wall("W-E", 8.0, 0.20, 2.80, brick)
    west = Wall("W-W", 8.0, 0.20, 2.80, brick)

    # One representative structural partition.
    partition = Wall("W-P1", 8.0, 0.10, 2.80, concrete)
    partition.add_opening(Opening("door", 0.80, 2.10, position_m=3.50))

    for wall in (south, north, east, west, partition):
        level.add_wall(wall)

    building.add_level(level)
    return building
