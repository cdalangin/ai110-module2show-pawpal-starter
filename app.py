from datetime import datetime

import streamlit as st
from pawpal_system import Owner, Pet, Scheduler, Task


def valid_time(text: str) -> bool:
    """Return True if text is a valid 24-hour HH:MM time."""
    try:
        datetime.strptime(text, "%H:%M")
    except ValueError:
        return False
    return True


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
availability = st.number_input("Time available today (minutes)", min_value=1, max_value=1440, value=90)

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name, availability=90)
owner = st.session_state.owner
owner.name = owner_name
owner.availability = int(availability)

if st.button("Add pet"):
    if any(p.name == pet_name for p in owner.pets):
        st.warning(f"{pet_name} already exists.")
    else:
        owner.pets.append(Pet(name=pet_name, species=species))
        st.success(f"Added {pet_name} the {species}.")

if owner.pets:
    st.write("Your pets: " + ", ".join(f"{p.name} ({p.species})" for p in owner.pets))


st.markdown("### Tasks")
st.caption("Give a task a preferred time (HH:MM) and set whether it repeats.")

task_pet = st.selectbox("Pet for this task", [p.name for p in owner.pets]) if owner.pets else None

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

col4, col5 = st.columns(2)
with col4:
    preferred_time = st.text_input("Preferred time (HH:MM, optional)", value="")
with col5:
    frequency = st.selectbox("Repeats", ["daily", "weekly", "once"])

if st.button("Add task"):
    time_text = preferred_time.strip()
    if task_pet is None:
        st.warning("Add a pet first.")
    elif time_text and not valid_time(time_text):
        st.warning("Preferred time must look like HH:MM, for example 08:30.")
    else:
        pet = next(p for p in owner.pets if p.name == task_pet)
        try:
            pet.add_task(
                Task(task_title, "general", int(duration), priority,
                     preference=time_text, frequency=frequency)
            )
        except ValueError as err:
            st.warning(str(err))
        else:
            st.success(f"Added '{task_title}' to {task_pet}.")

st.markdown("#### Your tasks")
if "flash" in st.session_state:
    st.success(st.session_state.pop("flash"))

all_tasks = owner.get_all_tasks()
if all_tasks:
    fcol1, fcol2 = st.columns(2)
    with fcol1:
        pet_filter = st.selectbox("Show pet", ["All pets"] + [p.name for p in owner.pets])
    with fcol2:
        status_filter = st.selectbox("Show status", ["All", "Pending", "Completed"])

    visible = Scheduler.sort_by_time(
        owner.filter_tasks(
            pet_name=None if pet_filter == "All pets" else pet_filter,
            completed={"All": None, "Pending": False, "Completed": True}[status_filter],
        )
    )
    if visible:
        st.caption(f"Showing {len(visible)} of {len(all_tasks)} task(s), sorted by time.")
        st.table(
            [
                {
                    "Pet": t.pet_name,
                    "Task": t.name,
                    "Time": t.preference or "—",
                    "Minutes": t.duration,
                    "Priority": t.priority,
                    "Repeats": t.frequency,
                    "Due": str(t.due_date) if t.due_date else "—",
                    "Status": "✅ Done" if t.completed else "Pending",
                }
                for t in visible
            ]
        )
    else:
        st.info("No tasks match these filters.")

    pending = Scheduler.sort_by_time(owner.filter_tasks(completed=False))
    if pending:
        choice = st.selectbox(
            "Mark a task complete",
            range(len(pending)),
            format_func=lambda i: f"{pending[i].pet_name}: {pending[i].name} ({pending[i].preference or 'any time'})",
        )
        if st.button("Complete task"):
            done = pending[choice]
            next_task = Scheduler(owner=owner).complete_task(done)
            msg = f"Completed '{done.name}' for {done.pet_name}."
            if next_task:
                msg += f" Next {next_task.frequency} occurrence is due {next_task.due_date:%b %d}."
            st.session_state.flash = msg
            st.rerun()
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Picks tasks by priority until time runs out, then lists them in time order.")

if st.button("Generate schedule"):
    scheduler = Scheduler(owner=owner)
    plan = scheduler.generate_plan()
    used = sum(t.duration for t in plan)

    if plan:
        st.success(f"Schedule generated: {len(plan)} task(s) planned.")
    else:
        st.info("Nothing to schedule. Add tasks that are pending and due today.")

    m1, m2, m3 = st.columns(3)
    m1.metric("Tasks planned", len(plan))
    m2.metric("Minutes used", f"{used} / {owner.availability}")
    m3.metric("Tasks skipped", len(scheduler.skipped_tasks))

    if plan:
        st.table(
            [
                {
                    "Time": t.preference or "—",
                    "Pet": t.pet_name,
                    "Task": t.name,
                    "Minutes": t.duration,
                    "Priority": t.priority,
                }
                for t in plan
            ]
        )

    for warning in scheduler.detect_conflicts():
        st.warning(warning)
    if scheduler.skipped_tasks:
        st.warning(
            "Skipped, not enough time: "
            + ", ".join(f"{t.name} ({t.pet_name}, {t.duration} min)" for t in scheduler.skipped_tasks)
        )

    with st.expander("Why this plan?"):
        st.text(scheduler.explain())
