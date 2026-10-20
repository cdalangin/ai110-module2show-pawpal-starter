import streamlit as st
from pawpal_system import Owner, Pet, Scheduler, Task

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

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name, availability=90)
owner = st.session_state.owner
owner.name = owner_name

if st.button("Add pet"):
    if any(p.name == pet_name for p in owner.pets):
        st.warning(f"{pet_name} already exists.")
    else:
        owner.pets.append(Pet(name=pet_name, species=species))
        st.success(f"Added {pet_name} the {species}.")

if owner.pets:
    st.write("Your pets: " + ", ".join(f"{p.name} ({p.species})" for p in owner.pets))

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

task_pet = st.selectbox("Pet for this task", [p.name for p in owner.pets]) if owner.pets else None

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    if task_pet is None:
        st.warning("Add a pet first.")
    else:
        pet = next(p for p in owner.pets if p.name == task_pet)
        pet.add_task(Task(task_title, "general", int(duration), priority))
        st.success(f"Added '{task_title}' to {task_pet}.")

all_tasks = owner.get_all_tasks()
if all_tasks:
    st.write("Current tasks:")
    st.table(
        [
            {"pet": t.pet_name, "title": t.name, "duration_minutes": t.duration, "priority": t.priority}
            for t in all_tasks
        ]
    )
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    scheduler = Scheduler(owner=owner)
    plan = scheduler.generate_plan()
    st.success(f"Schedule generated: {len(plan)} task(s) planned.")
    st.table(
        [{"pet": t.pet_name, "task": t.name, "minutes": t.duration, "priority": t.priority} for t in plan]
    )
    st.text(scheduler.explain())
