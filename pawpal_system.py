from dataclasses import dataclass, field


@dataclass
class Task:
    name: str
    category: str
    duration: int
    priority: str
    preference: str = ""
    frequency: str = "daily"
    completed: bool = False

    def mark_complete(self) -> None:
        self.completed = True


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)


@dataclass
class Owner:
    name: str
    availability: int
    pets: list[Pet] = field(default_factory=list)
    preferences: dict = field(default_factory=dict)

    def get_all_tasks(self) -> list[Task]:
        return [task for pet in self.pets for task in pet.tasks]


@dataclass
class Plan:
    scheduled_items: list[Task] = field(default_factory=list)
    skipped_tasks: list[Task] = fie

    def explain(self) -> str:
        pass
