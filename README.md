# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
  + Morning walk for Biscuit at 08:00: high priority, fits in 30 min.
  + Feeding for Whiskers at 09:00: high priority, fits in 10 min.
  + Medication for Whiskers at 13:00: high priority, fits in 5 min.
  + Play session for Whiskers at 16:30: medium priority, fits in 20 min.
  - Grooming for Biscuit skipped: needs 45 min (low priority) but not enough time remained.
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
python -m pytest
```

### What the tests cover

The 17 tests in [tests/test_pawpal.py](tests/test_pawpal.py) check the scheduling behavior:

- **Tasks and pets:** marking a task complete, and adding tasks to a pet.
- **Input checks:** a zero or negative duration and an unknown priority are rejected; a duplicate task name is rejected for the same pet but allowed for a different pet, and a completed task's name can be reused.
- **Sorting:** `Scheduler.sort_by_time()` puts tasks in chronological order (`"8:30"` before `"09:15"`) with untimed tasks last, and `generate_plan()` returns its tasks in time order even when priorities differ, including after some tasks are dropped for lack of time.
- **Filtering:** `Owner.filter_tasks()` by pet name, by completion status, by both, and for an unknown pet.
- **Recurring tasks:** completing a daily task creates a new task due the next day, a weekly task is due 7 days after its due date, a one-off task does not recur, and the next occurrence stays out of today's plan.
- **Conflict detection:** `Scheduler.detect_conflicts()` flags tasks at the same time for one pet and for different pets (treating `"8:00"` and `"08:00"` as the same), and returns nothing when there are no clashes.

### Test results

```
============================= test session starts =============================
platform win32 -- Python 3.14.7, pytest-9.1.1, pluggy-1.7.0
rootdir: C:\Users\ishad\Desktop\justcodingthingz\Codepath\AIClass\ai110-module2show-pawpal-starter
plugins: anyio-4.15.1
collected 17 items

tests\test_pawpal.py .................                                   [100%]

============================= 17 passed in 0.05s ==============================
```

### Confidence level: ★★★★★ (5 / 5)

All 17 tests pass, and they cover the core logic, which are sorting, filtering, recurrence, conflict detection and input checks, including edge cases like untimed tasks, unpadded times and one-off tasks. 

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | | e.g., by priority, duration |
| Filtering | | e.g., skip tasks if time runs out |
| Conflict handling | | e.g., overlapping time slots |
| Recurring tasks | | e.g., daily vs. weekly |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->

## Implementation Sumamry
The Owner class holds a list of Pet objects and a daily availability in minutes, and each Pet holds its own Task objects (name, category, duration, priority, preferred time, completion status). A Scheduler takes an Owner, gathers all of their pets' incomplete tasks, picks them by priority (high, then medium, then low) until the owner's available minutes run out, and sorts the chosen tasks by preferred time. It keeps the scheduled and skipped tasks in two lists, and its explain() method turns those lists into a plain-text reason for each decision, which main.py prints as "Today's Schedule" and "Why this plan?"

## Smart Scheduling

### Sorting by time: `Scheduler.sort_by_time(tasks)`

Orders tasks by their preferred `HH:MM` time, earliest first. The sort key is a lambda that turns each time into an `(hour, minute)` integer tuple, so `"8:30"` sorts before `"09:15"` (comparing the raw strings would get that wrong). Tasks with no preferred time go last. It returns a new list and does not change the one you pass in.

`generate_plan()` uses it to put the chosen tasks in time order. Priority still decides *which* tasks make it into the plan (highest first, until the owner's minutes run out); preferred time only decides the order they appear in.

### Filtering: `Owner.filter_tasks(pet_name=None, completed=None)`

Returns the tasks across all of an owner's pets that match the filters you give:

- `pet_name` keeps one pet's tasks. The match ignores case, so `"rex"` finds `"Rex"`.
- `completed=True` keeps finished tasks and `completed=False` keeps pending ones.
- A filter left as `None` is ignored, and passing both requires both to match.

`Owner.get_all_tasks()` is the unfiltered version. The results keep the order tasks were added, so pass them to `Scheduler.sort_by_time()` to order them by time. `generate_plan()` also leaves out completed tasks and tasks whose `due_date` is still in the future.

### Conflict detection: `Scheduler.detect_conflicts()`

A lightweight check that returns warning messages and never raises or changes the plan. Call it after `generate_plan()`. It groups the scheduled tasks by start time and reports every time that has more than one task, whether they belong to the same pet or to different pets:

```
Warning: 2 tasks at 8:00: Morning walk (Biscuit), Flea treatment (Biscuit)
Warning: 2 tasks at 09:00: Vet call (Biscuit), Feeding (Whiskers)
```

Times are compared as numbers, so `"8:00"` and `"08:00"` count as the same time. Tasks with no preferred time are ignored. **Tradeoff:** it only catches identical start times. A 30-minute walk at 08:00 and a feeding at 08:15 overlap but are not flagged.

### Recurring tasks: `Scheduler.complete_task(task)`

Marks a task complete and, if its `frequency` is `"daily"` or `"weekly"`, adds the next occurrence to the same pet. The new task is an incomplete copy with a `due_date` one step later, computed with `timedelta` (`timedelta(days=1)` or `timedelta(weeks=1)`), so month, year and leap-day rollover are handled. The step is added to the task's own `due_date`, or to today if it has none, so a weekly task finished late stays on its weekly rhythm. Other frequencies, such as `"once"`, do not recur and the method returns `None`.

`generate_plan()` skips tasks whose `due_date` is still in the future, so completing today's walk does not put tomorrow's walk back in today's plan. Call `complete_task()` rather than `Task.mark_complete()` when you want recurrence, because only the scheduler knows which pet owns the task.

### Input checks

- `Task` rejects a duration of zero or less and any priority other than `high`, `medium` or `low`.
- `Pet.add_task()` rejects a second incomplete task with the same name for the same pet (ignoring case). Two different pets can share a task name.
