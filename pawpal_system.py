from dataclasses import dataclass, field


@dataclass
class Task:
    name: str
    category: str
    duration: int
    priority: str
    pet_name: str = ""
    preference: str = ""
    frequency: str = "daily"
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.completed = True


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet and record the pet's name on it."""
        task.pet_name = self.name
        self.tasks.append(task)


@dataclass
class Owner:
    name: str
    availability: int
    pets: list[Pet] = field(default_factory=list)
    preferences: dict = field(default_factory=dict)

    def get_all_tasks(self) -> list[Task]:
        """Return every task across all of the owner's pets."""
        return [task for pet in self.pets for task in pet.tasks]


@dataclass
class Scheduler:
    owner: Owner
    scheduled_items: list[Task] = field(default_factory=list)
    skipped_tasks: list[Task] = field(default_factory=list)

    def generate_plan(self) -> list[Task]:
        """Pick incomplete tasks by priority within available time, ordered by preferred time."""
        rank = {"high": 0, "medium": 1, "low": 2}
        by_priority = sorted(
            (t for t in self.owner.get_all_tasks() if not t.completed),
            key=lambda t: rank.get(t.priority, 3),
        )
        self.scheduled_items = []
        self.skipped_tasks = []
        minutes_left = self.owner.availability
        for task in by_priority:
            if task.duration <= minutes_left:
                self.scheduled_items.append(task)
                minutes_left -= task.duration
            else:
                self.skipped_tasks.append(task)
        self.scheduled_items.sort(key=lambda t: t.preference or "99:99")
        return self.scheduled_items

    def explain(self) -> str:
        """Return a text explanation of why tasks were scheduled or skipped."""
        used = sum(t.duration for t in self.scheduled_items)
        available = self.owner.availability
        lines = [
            f"{self.owner.name} has {available} minutes available today. "
            f"Tasks were chosen by priority (high, then medium, then low) "
            f"until time ran out, then ordered by preferred time.",
            f"Scheduled {used} of {available} minutes ({available - used} left).",
        ]
        for t in self.scheduled_items:
            when = f" at {t.preference}" if t.preference else ""
            lines.append(
                f"  + {t.name} for {t.pet_name}{when}: "
                f"{t.priority} priority, fits in {t.duration} min."
            )
        for t in self.skipped_tasks:
            lines.append(
                f"  - {t.name} for {t.pet_name} skipped: needs {t.duration} min "
                f"({t.priority} priority) but not enough time remained."
            )
        return "\n".join(lines)
