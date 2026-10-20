from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    owner = Owner(name="Jordan", availability=90)

    biscuit = Pet(name="Biscuit", species="Dog")
    whiskers = Pet(name="Whiskers", species="Cat")
    owner.pets.extend([biscuit, whiskers])

    biscuit.add_task(Task("Morning walk", "walk", 30, "high", preference="08:00"))
    biscuit.add_task(Task("Grooming", "grooming", 45, "low", preference="18:00"))
    whiskers.add_task(Task("Feeding", "food", 10, "high", preference="09:00"))
    whiskers.add_task(Task("Medication", "medication", 5, "high", preference="13:00"))
    whiskers.add_task(Task("Play session", "enrichment", 20, "medium", preference="16:30"))

    scheduler = Scheduler(owner=owner)
    plan = scheduler.generate_plan()

    print(f"Today's Schedule for {owner.name} ({owner.availability} min available)")
    print("-" * 50)
    for task in plan:
        print(
            f"{task.preference} - {task.name} for {task.pet_name} "
            f"({task.duration} min) [priority: {task.priority}]"
        )

    if scheduler.skipped_tasks:
        print("\nSkipped (not enough time):")
        for task in scheduler.skipped_tasks:
            print(f"  {task.name} for {task.pet_name} ({task.duration} min)")

    print("\nWhy this plan?")
    print(scheduler.explain())


if __name__ == "__main__":
    main()
