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


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)


@dataclass
class Owner:
    name: str
    availability: int
    pets: list[Pet] = field(default_factory=list)
    preferences: dict = field(default_factory=dict)


@dataclass
class Plan:
    scheduled_items: list[Task] = field(default_factory=list)
    skipped_tasks: list[Task] = field(default_factory=list)

    def explain(self) -> str:
        pass
