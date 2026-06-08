"""Test that all public API classes are properly importable."""


def test_task_output_import():
    """Test that TaskOutput can be imported from fzxiezuoai."""
    from fzxiezuoai import TaskOutput

    assert TaskOutput is not None


def test_crew_output_import():
    """Test that CrewOutput can be imported from fzxiezuoai."""
    from fzxiezuoai import CrewOutput

    assert CrewOutput is not None
