from dataclasses import dataclass, field, replace
from datetime import date, timedelta

PRIORITIES = ("high", "medium", "low")
RECURRENCE = {"daily": timedelta(days=1), "weekly": timedelta(weeks=1)}


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
    due_date: date | None = None

    def __post_init__(self) -> None:
        """Reject non-positive durations and unknown priorities."""
        if self.duration <= 0:
            raise ValueError(f"Duration must be positive, got {self.duration}.")
        if self.priority not in PRIORITIES:
            raise ValueError(f"Priority must be one of {PRIORITIES}, got '{self.priority}'.")

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.completed = True


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet and record the pet's name on it.

        Raises ValueError if the pet already has an incomplete task with the same name.
        """
        if any(t.name.lower() == task.name.lower() and not t.completed for t in self.tasks):
            raise ValueError(f"{self.name} already has a task named '{task.name}'.")
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

    def filter_tasks(self, pet_name: str | None = None, completed: bool | None = None) -> list[Task]:
        """Return tasks matching the given pet name and/or completion status.

        Args:
            pet_name: keep only this pet's tasks (case-insensitive); None means any pet.
            completed: True for finished tasks, False for pending ones; None means both.
        A filter left as None is ignored; passing both requires both to match.
        Returns: matching tasks in the order they were added (empty if none match).
        """
        return [
            t for t in self.get_all_tasks()
            if (pet_name is None or t.pet_name.lower() == pet_name.lower())
            and (completed is None or t.completed == completed)
        ]


@dataclass
class Scheduler:
    owner: Owner
    scheduled_items: list[Task] = field(default_factory=list)
    skipped_tasks: list[Task] = field(default_factory=list)

    def generate_plan(self) -> list[Task]:
        """Build today's plan from the owner's tasks and store it on the scheduler.

        Algorithm (greedy):
          1. Keep tasks that are not completed and are not due in the future.
          2. Sort them high -> medium -> low priority (stable, so ties keep their order).
          3. Walk the list, taking each task that still fits in the remaining minutes
             of the owner's availability; tasks that don't fit are skipped.
          4. Order the chosen tasks by preferred time with sort_by_time.

        Side effects: replaces scheduled_items and skipped_tasks.
        Returns: the scheduled tasks, in time order.
        """
        by_priority = sorted(
            (
                t for t in self.owner.get_all_tasks()
                if not t.completed and (t.due_date is None or t.due_date <= date.today())
            ),
            key=lambda t: PRIORITIES.index(t.priority),
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
        self.scheduled_items = self.sort_by_time(self.scheduled_items)
        return self.scheduled_items

    def detect_conflicts(self) -> list[str]:
        """Warn about scheduled tasks that share the same start time.

        Lightweight check: scheduled_items are grouped by their 'HH:MM' preference
        (compared as numbers, so '8:00' and '08:00' count as the same time) and
        each group with more than one task yields a message. It works across pets
        and within one pet. Tasks without a preferred time are ignored, and only
        identical start times count: overlapping but different times are not flagged.

        Call after generate_plan. Nothing is raised or rearranged.
        Returns: one warning string per clashing time, or an empty list.
        """
        by_start: dict[tuple[int, ...], list[Task]] = {}
        for t in self.scheduled_items:
            if t.preference:
                start = tuple(int(part) for part in t.preference.split(":"))
                by_start.setdefault(start, []).append(t)
        return [
            f"Warning: {len(group)} tasks at {group[0].preference}: "
            + ", ".join(f"{t.name} ({t.pet_name})" for t in group)
            for group in by_start.values()
            if len(group) > 1
        ]

    def complete_task(self, task: Task) -> Task | None:
        """Mark a task complete and, if it recurs, add its next occurrence to the same pet.

        Daily and weekly tasks get a fresh, incomplete copy whose due_date is one
        timedelta step (1 day or 7 days) after the task's own due_date, or after
        today when it had none. Using timedelta handles month, year and leap-day
        rollover. Any other frequency (e.g. 'once') does not recur.

        Args:
            task: a task belonging to one of the owner's pets.
        Returns: the newly created task, or None if the task does not recur.
        """
        task.mark_complete()
        step = RECURRENCE.get(task.frequency)
        if step is None:
            return None
        next_task = replace(task, completed=False, due_date=(task.due_date or date.today()) + step)
        pet = next(p for p in self.owner.pets if p.name == task.pet_name)
        pet.add_task(next_task)
        return next_task

    @staticmethod
    def sort_by_time(tasks: list[Task]) -> list[Task]:
        """Return tasks ordered by their 'HH:MM' preference, earliest first.

        The sort key is a lambda that turns 'HH:MM' into an (hour, minute) integer
        tuple, so '8:30' sorts before '09:15' (plain string comparison would not).
        Tasks with no preference get (24, 0) and sort last. The sort is stable and
        returns a new list; the input is not modified.

        Args:
            tasks: tasks whose preference is blank or a valid 'HH:MM' string.
        """
        return sorted(
            tasks,
            key=lambda t: tuple(int(part) for part in t.preference.split(":")) if t.preference else (24, 0),
        )

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
