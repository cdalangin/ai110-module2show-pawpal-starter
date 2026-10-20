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

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Priority-based planning | `Scheduler.generate_plan()` | Takes tasks from high to low priority until the owner's available minutes run out; tasks that don't fit are skipped, so the least important ones are dropped. |
| Task sorting | `Scheduler.sort_by_time()` | Orders tasks by preferred time using real hours and minutes, so 8:30 comes before 9:15. Tasks with no time go last. |
| Filtering | `Owner.filter_tasks()` | Narrows tasks by pet, by pending or completed status, or both. Pet names ignore capitalization. |
| Conflict handling | `Scheduler.detect_conflicts()` | Warns when tasks share a start time, for one pet or across pets. Only warns, never changes the plan. Does not catch partial overlaps. |
| Recurring tasks | `Scheduler.complete_task()` | Completing a daily or weekly task creates the next occurrence using date arithmetic that handles month ends, year ends and leap days. One-time tasks don't repeat. |
| Future tasks held back | `Scheduler.generate_plan()` | A repeating task's next occurrence is only planned once its due date arrives. |
| Completed tasks excluded | `Scheduler.generate_plan()` | Finished tasks are never scheduled again. |
| Duplicate prevention | `Pet.add_task()` | A pet can't have two pending tasks with the same name. Different pets can share a name, and a completed task's name can be reused. |
| Input validation | `Task.__post_init__()` | Rejects a zero or negative duration and an unrecognized priority. The app also rejects a preferred time that isn't a valid HH:MM. |
| Plan explanations | `Scheduler.explain()` | Gives a plain-language reason for each scheduled or skipped task, including how many available minutes were used. |

## 📸 Demo Walkthrough

### What you can do in the app

- Enter the owner's name and how many minutes they have available today.
- Add pets, each with a name and species.
- Add tasks to a pet with a title, duration, priority, optional preferred time and a repeat setting of daily, weekly or once.
- View all tasks sorted by time, and filter them by pet or by pending and completed status.
- Mark a task complete, which automatically creates the next occurrence for daily and weekly tasks.
- Generate a schedule that shows the planned tasks, minutes used, any conflict warnings, any skipped tasks and an explanation of the plan.

### Example workflow

1. Enter the owner's name and available minutes, then add a pet such as Biscuit the dog.
2. Add a few tasks for Biscuit, such as a morning walk at 08:00 and grooming at 18:00, in any order.
3. Use the pet and status filters to check the task list, which is always shown in time order.
4. Click "Generate schedule" to see today's plan, with a warning if two tasks share a start time and a note on anything that was skipped.
5. Mark the walk complete and see the next day's walk appear as a new task that stays out of today's plan.

### Scheduler behaviors on display

- Tasks are picked by priority until the available time runs out, so lower-priority tasks are the ones skipped.
- The final plan is sorted by time, with untimed tasks at the end.
- Tasks at the same start time trigger a warning, whether they belong to one pet or to different pets.
- Completing a daily or weekly task creates the next occurrence, and finished tasks never reappear in the plan.
- The plan comes with a plain-language explanation of every task that was scheduled or skipped.

### Sample output from main.py

```
All tasks, in the order they were added:
  18:00  Grooming (Biscuit, 45 min, done)
  8:00  Morning walk (Biscuit, 30 min, pending)
  --:--  Brush teeth (Biscuit, 5 min, pending)
  08:00  Flea treatment (Biscuit, 5 min, pending)
  09:00  Vet call (Biscuit, 10 min, pending)
  16:30  Play session (Whiskers, 20 min, done)
  13:00  Medication (Whiskers, 5 min, pending)
  09:00  Feeding (Whiskers, 10 min, pending)

All tasks, sorted by time:
  8:00  Morning walk (Biscuit, 30 min, pending)
  08:00  Flea treatment (Biscuit, 5 min, pending)
  09:00  Vet call (Biscuit, 10 min, pending)
  09:00  Feeding (Whiskers, 10 min, pending)
  13:00  Medication (Whiskers, 5 min, pending)
  16:30  Play session (Whiskers, 20 min, done)
  18:00  Grooming (Biscuit, 45 min, done)
  --:--  Brush teeth (Biscuit, 5 min, pending)

Biscuit's tasks:
  18:00  Grooming (Biscuit, 45 min, done)
  8:00  Morning walk (Biscuit, 30 min, pending)
  --:--  Brush teeth (Biscuit, 5 min, pending)
  08:00  Flea treatment (Biscuit, 5 min, pending)
  09:00  Vet call (Biscuit, 10 min, pending)

Whiskers' tasks, sorted by time:
  09:00  Feeding (Whiskers, 10 min, pending)
  13:00  Medication (Whiskers, 5 min, pending)
  16:30  Play session (Whiskers, 20 min, done)

Pending tasks:
  8:00  Morning walk (Biscuit, 30 min, pending)
  --:--  Brush teeth (Biscuit, 5 min, pending)
  08:00  Flea treatment (Biscuit, 5 min, pending)
  09:00  Vet call (Biscuit, 10 min, pending)
  13:00  Medication (Whiskers, 5 min, pending)
  09:00  Feeding (Whiskers, 10 min, pending)

Completed tasks:
  18:00  Grooming (Biscuit, 45 min, done)
  16:30  Play session (Whiskers, 20 min, done)

Whiskers' pending tasks, sorted by time:
  09:00  Feeding (Whiskers, 10 min, pending)
  13:00  Medication (Whiskers, 5 min, pending)

Today's Schedule for Jordan (90 min available)
--------------------------------------------------
8:00 - Morning walk for Biscuit (30 min) [priority: high]
08:00 - Flea treatment for Biscuit (5 min) [priority: high]
09:00 - Vet call for Biscuit (10 min) [priority: high]
09:00 - Feeding for Whiskers (10 min) [priority: high]
13:00 - Medication for Whiskers (5 min) [priority: high]
--:-- - Brush teeth for Biscuit (5 min) [priority: low]

Conflict check:
  Warning: 2 tasks at 8:00: Morning walk (Biscuit), Flea treatment (Biscuit)
  Warning: 2 tasks at 09:00: Vet call (Biscuit), Feeding (Whiskers)

Why this plan?
Jordan has 90 minutes available today. Tasks were chosen by priority (high, then medium, then low) until time ran out, then ordered by preferred time.
Scheduled 65 of 90 minutes (25 left).
  + Morning walk for Biscuit at 8:00: high priority, fits in 30 min.
  + Flea treatment for Biscuit at 08:00: high priority, fits in 5 min.
  + Vet call for Biscuit at 09:00: high priority, fits in 10 min.
  + Feeding for Whiskers at 09:00: high priority, fits in 10 min.
  + Medication for Whiskers at 13:00: high priority, fits in 5 min.
  + Brush teeth for Biscuit: low priority, fits in 5 min.
```

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
