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


import pytest


def test_duplicate_task_name_rejected_for_same_pet_only():
    rex, tom = Pet("Rex", "dog"), Pet("Tom", "cat")
    rex.add_task(Task("Walk", "walk", 20, "high"))

    with pytest.raises(ValueError):
        rex.add_task(Task("walk", "walk", 20, "high"))
    tom.add_task(Task("Walk", "walk", 20, "high"))
    assert len(rex.tasks) == 1 and len(tom.tasks) == 1


def test_completed_task_name_can_be_reused():
    pet = Pet("Rex", "dog")
    first = Task("Walk", "walk", 20, "high")
    pet.add_task(first)
    first.mark_complete()
    pet.add_task(Task("Walk", "walk", 20, "high"))
    assert len(pet.tasks) == 2


@pytest.mark.parametrize("duration, priority", [(0, "high"), (-5, "low"), (10, "hgih")])
def test_invalid_task_inputs_rejected(duration, priority):
    with pytest.raises(ValueError):
        Task("x", "general", duration, priority)


from pawpal_system import Scheduler


def test_sort_by_time_orders_chronologically_with_untimed_last():
    tasks = [
        Task("none", "x", 5, "low"),
        Task("pm", "x", 5, "low", preference="13:00"),
        Task("early", "x", 5, "low", preference="8:30"),
        Task("am", "x", 5, "low", preference="09:15"),
    ]
    assert [t.name for t in Scheduler.sort_by_time(tasks)] == ["early", "am", "pm", "none"]


from pawpal_system import Owner


def test_filter_tasks_by_pet_and_status():
    owner = Owner("J", 60)
    dog, cat = Pet("Rex", "dog"), Pet("Tom", "cat")
    owner.pets += [dog, cat]
    walk = Task("walk", "walk", 10, "high")
    dog.add_task(walk)
    dog.add_task(Task("bath", "groom", 10, "low"))
    cat.add_task(Task("feed", "food", 5, "high"))
    walk.mark_complete()

    names = lambda tasks: [t.name for t in tasks]
    assert names(owner.filter_tasks()) == ["walk", "bath", "feed"]
    assert names(owner.filter_tasks(pet_name="rex")) == ["walk", "bath"]
    assert names(owner.filter_tasks(completed=False)) == ["bath", "feed"]
    assert names(owner.filter_tasks(pet_name="Rex", completed=True)) == ["walk"]
    assert owner.filter_tasks(pet_name="Nobody") == []


from datetime import date, timedelta


def _owner_with(task):
    owner = Owner("J", 60)
    pet = Pet("Rex", "dog")
    owner.pets.append(pet)
    pet.add_task(task)
    return owner, pet


def test_completing_daily_task_creates_next_day_instance():
    task = Task("walk", "walk", 20, "high", preference="08:00", frequency="daily")
    owner, pet = _owner_with(task)

    nxt = Scheduler(owner).complete_task(task)

    assert task.completed and nxt is not task
    assert not nxt.completed and nxt.due_date == date.today() + timedelta(days=1)
    assert (nxt.name, nxt.preference, nxt.pet_name) == ("walk", "08:00", "Rex")
    assert pet.tasks == [task, nxt]


def test_completing_weekly_task_adds_seven_days_from_its_due_date():
    due = date.today() + timedelta(days=2)
    task = Task("bath", "groom", 20, "low", frequency="weekly", due_date=due)
    owner, _ = _owner_with(task)

    assert Scheduler(owner).complete_task(task).due_date == due + timedelta(weeks=1)


def test_completing_one_off_task_does_not_recur():
    task = Task("vet", "health", 30, "high", frequency="once")
    owner, pet = _owner_with(task)

    assert Scheduler(owner).complete_task(task) is None
    assert pet.tasks == [task]


def test_next_occurrence_not_planned_until_due():
    task = Task("walk", "walk", 20, "high", frequency="daily")
    owner, _ = _owner_with(task)
    scheduler = Scheduler(owner)

    scheduler.complete_task(task)

    assert scheduler.generate_plan() == []


def test_detect_conflicts_same_pet_and_different_pets():
    owner = Owner("J", 120)
    rex, tom = Pet("Rex", "dog"), Pet("Tom", "cat")
    owner.pets += [rex, tom]
    rex.add_task(Task("walk", "walk", 10, "high", preference="8:00"))
    rex.add_task(Task("meds", "med", 5, "high", preference="08:00"))
    rex.add_task(Task("bath", "groom", 5, "high", preference="12:00"))
    tom.add_task(Task("feed", "food", 5, "high", preference="12:00"))
    tom.add_task(Task("play", "fun", 5, "high", preference="15:00"))
    tom.add_task(Task("brush", "groom", 5, "low"))
    scheduler = Scheduler(owner)
    scheduler.generate_plan()

    warnings = scheduler.detect_conflicts()

    assert len(warnings) == 2
    assert "walk (Rex)" in warnings[0] and "meds (Rex)" in warnings[0]
    assert "bath (Rex)" in warnings[1] and "feed (Tom)" in warnings[1]


def test_detect_conflicts_empty_when_no_clashes():
    owner = Owner("J", 60)
    pet = Pet("Rex", "dog")
    owner.pets.append(pet)
    pet.add_task(Task("walk", "walk", 10, "high", preference="08:00"))
    pet.add_task(Task("feed", "food", 5, "high"))
    scheduler = Scheduler(owner)
    scheduler.generate_plan()

    assert scheduler.detect_conflicts() == []
