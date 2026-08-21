from lat_ces.gui_master import MasterBuildingWorkspaceApp


def test_master_command_callbacks_exist():
    required = (
        "_load_reference_house",
        "_show_view",
        "_run_master_validation",
        "_show_engineering_report",
        "_refresh_master_metrics",
        "_refresh_level_selector",
    )
    for name in required:
        assert callable(getattr(MasterBuildingWorkspaceApp, name, None)), name


def test_reference_house_loader_is_canonical_workflow_entrypoint():
    method = MasterBuildingWorkspaceApp._load_reference_house
    assert "build_reference_house_workflow" in method.__code__.co_names
