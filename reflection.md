# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
    - Users should be a ble to add pet and owner information
    - Users should be able to add and edit tasks for their pet
    - Users should be able to view a daily plan
- What classes did you include, and what responsibilities did you assign to each?
    - Owner
        - Name
        - Pets
        - Preferences
        - Availability
        - get_all_tasks()
    - Pet
        - Name
        - Species
        - Tasks
        - add_task()
    - Scheduler
        - Owner
        - Scheduled items
        - Skipped Tasks
        - generate_plan()
        - explain()
    - Task
        - Name
        - Category
        - Duration
        - Priority
        - Pet name
        - Preference
        - Frequency
        - Completed
        - mark_complete() 

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
    - Scheduler didn't have a function that would generate a plan consisting of a list of items so the AI gave a suggestion to include that, and I think this makes sense for the requirement that generates a daily schedule

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
    - First constraint is the owner's availability, so only tasks that can fit in that time will be added
    - Next is priority because the user intentionally set that constraint, so the algorithm will follow it
- How did you decide which constraints mattered most?
    - Logistically, the time constraint has to be the most important thing because if the owner set that they only have that amount of time to work, the algorithm should follow that

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
    - The generate_plan function sorts by priority and takes each task that still fits in the remaining minutes, instead of checking if there's an option where more tasks can be added, it would just start with high priority tasks and go from there
- Why is that tradeoff reasonable for this scenario?
    - It would be much easier to explain the plan and would mean writing more code
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
    - I used the AI to check the classes I built to see if the relationships make sense. It also helped with brainstorming where to put the lists of other classes, like for example putting the list of tasks in Pets instead of the Owner since it could potentially vary from pet to pet
- What kinds of prompts or questions were most helpful?
    - I think the 

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
    - It originally just suggested to make the scheduler with the generate_plan() function with no other fields, I asked if there are other fields that need to be added
- How did you evaluate or verify what the AI suggested?
    - I read through the requirements again and noticed we also need to mention skilled plans and skipped tasks

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
