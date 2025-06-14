from src.domain.task import Task


def test_tag_operations():
    task = Task("Learn Python")
    task.add_tag("education")
    assert "education" in task.tags
    assert "Tag added" in task.history[-1]

    task.remove_tag("education")
    assert "education" not in task.tags
    assert "Tag removed" in task.history[-1]


def test_tag_validation():
    task = Task("Test")
    try:
        task.add_tag("a")
        assert False, "Validation should fail for short tag"
    except ValueError:
        pass