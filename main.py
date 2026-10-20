from pawpal_system import Owner, Pet, Scheduler, Task


def show(title: str, tasks: list[Task]) -> None:
    print(f"\n{title}")
    if not tasks:
        print("  (none)")
    for t in tasks:
        status = "done" if t.completed else "pending"
        print(f"  {t.preference or '--:--'}  {t.name} ({t.pet_name}, {t.duration} min, {status})")


def main() -> None:
    owner = Owner(name="Jordan", availability=90)

    biscuit = Pet(name="Biscuit", species="Dog")
    whiskers = Pet(name="Whiskers", species="Cat")
    owner.pets.extend([biscuit, whiskers])

    # Added deliberately out of chronological order.
    biscuit.add_task(Task("Grooming", "grooming", 45, "low", preference="18:00"))
    whiskers.add_task(Task("Play session", "enrichment", 20, "medium", preference="16:30"))
    biscuit.add_task(Task("Morning walk", "walk", 30, "high", preference="8:00"))
    whiskers.add_task(Task("Medication", "medication", 5, "high", preference="13:00"))
    whiskers.add_task(Task("Feeding", "food", 10, "high", preference="09:00"))
    biscuit.add_task(Task("Brush teeth", "grooming", 5, "low"))  # no preferred time

    # Deliberate conflicts: same pet (Biscuit at 8:00) and different pets (09:00).
    biscuit.add_task(Task("Flea treatment", "medication", 5, "high", preference="08:00"))
    biscuit.add_task(Task("Vet call", "health", 10, "high", preference="09:00"))

    # Mark a couple done so the status filter has something to show.
    owner.filter_tasks(pet_name="Whiskers")[0].mark_complete()  # Play session
    biscuit.tasks[0].mark_complete()  # Grooming

    show("All tasks, in the order they were added:", owner.get_all_tasks())
    show("All tasks, sorted by time:", Scheduler.sort_by_time(owner.get_all_tasks()))
    show("Biscuit's tasks:", owner.filter_tasks(pet_name="Biscuit"))
    show("Whiskers' tasks, sorted by time:", Scheduler.sort_by_time(owner.filter_tasks(pet_name="Whiskers")))
    show("Pending tasks:", owner.filter_tasks(completed=False))
    show("Completed tasks:", owner.filter_tasks(completed=True))
    show("Whiskers' pending tasks, sorted by time:", Scheduler.sort_by_time(
        owner.filter_tasks(pet_name="Whiskers", completed=False)))

    scheduler = Scheduler(owner=owner)
    plan = scheduler.generate_plan()

    print(f"\nToday's Schedule for {owner.name} ({owner.availability} min available)")
    print("-" * 50)
    for task in plan:
        print(
            f"{task.preference or '--:--'} - {task.name} for {task.pet_name} "
            f"({task.duration} min) [priority: {task.priority}]"
        )

    conflicts = scheduler.detect_conflicts()
    print("\nConflict check:")
    for warning in conflicts or ["No conflicts."]:
        print(f"  {warning}")

    if scheduler.skipped_tasks:
        print("\nSkipped (not enough time):")
        for task in scheduler.skipped_tasks:
            print(f"  {task.name} for {task.pet_name} ({task.duration} min)")

    print("\nWhy this plan?")
    print(scheduler.explain())


if __name__ == "__main__":
    main()
