from pawpal_system import Pet, Task


def test_mark_complete_changes_task_status():
    task = Task("Morning walk", "walk", 30, "high")
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Biscuit", species="Dog")
    assert len(pet.tasks) == 0

    pet.add_task(Task("Feeding", "food", 10, "high"))
    assert len(pet.tasks) == 1

    pet.add_task(Task("Grooming", "grooming", 45, "low"))
    assert len(pet.tasks) == 2
