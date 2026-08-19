from lat_ces.gui_theme import COLORS, apply_latces_theme
from lat_ces.gui_master import MasterBuildingWorkspaceApp


def test_master_gui_entrypoint_imports_without_creating_a_window():
    assert MasterBuildingWorkspaceApp.__name__ == "MasterBuildingWorkspaceApp"
    assert COLORS["primary"] == "#2563EB"
    assert callable(apply_latces_theme)
