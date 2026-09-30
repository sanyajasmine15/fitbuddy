import random
from html import escape

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

from database import SessionLocal, FitnessPlan


app = FastAPI(title="FitBuddy - AI Fitness Plan Generator")


# ============================================================
# FITBUDDY LOCAL AI-STYLE PLAN GENERATOR
# ============================================================

def generate_local_plan(name, age, goal, intensity, feedback=None):
    """
    Generates a detailed 7-day wellness plan locally.

    No Gemini API.
    No API key.
    No internet AI service.
    """

    name = str(name).strip()
    goal = str(goal).strip()
    intensity = str(intensity).strip()

    # Safe interpretation of intensity
    if intensity.lower() == "high":
        intensity_label = "Comfortable / Higher Activity Preference"
        session_time = "15–20 minutes"
        repetitions = "6–10 comfortable repetitions"
    elif intensity.lower() == "moderate":
        intensity_label = "Moderate"
        session_time = "12–18 minutes"
        repetitions = "5–8 comfortable repetitions"
    else:
        intensity_label = "Low / Gentle"
        session_time = "8–15 minutes"
        repetitions = "4–8 comfortable repetitions"

    # --------------------------------------------------------
    # Activity libraries
    # --------------------------------------------------------

    warmups = [
        [
            "Gentle marching in place for 2–3 minutes.",
            "Slow shoulder rolls.",
            "Gentle ankle circles.",
            "Relaxed arm movements."
        ],
        [
            "Slow walking around the room.",
            "Gentle shoulder movements.",
            "Easy wrist and ankle movements.",
            "Slow breathing for a few moments."
        ],
        [
            "March gently in place.",
            "Move both arms comfortably.",
            "Perform gentle shoulder circles.",
            "Move the ankles through a comfortable range."
        ]
    ]

    full_body = [
        [
            "Chair sit-to-stand",
            "Wall push-ups",
            "Standing calf raises",
            "Comfortable walking"
        ],
        [
            "Gentle marching",
            "Wall push-ups",
            "Chair sit-to-stand",
            "Standing arm movements"
        ],
        [
            "Comfortable walking",
            "Supported calf raises",
            "Wall push-ups",
            "Gentle full-body stretching"
        ]
    ]

    upper_body = [
        [
            "Wall push-ups",
            "Seated arm raises",
            "Shoulder rolls",
            "Gentle wrist movements"
        ],
        [
            "Wall push-ups",
            "Standing arm reaches",
            "Seated shoulder movements",
            "Gentle upper-body stretching"
        ],
        [
            "Seated arm raises",
            "Wall push-ups",
            "Shoulder mobility",
            "Gentle arm stretches"
        ]
    ]

    lower_body = [
        [
            "Chair sit-to-stand",
            "Supported calf raises",
            "Small side steps",
            "Gentle leg stretching"
        ],
        [
            "Chair sit-to-stand",
            "Supported heel raises",
            "Comfortable walking",
            "Gentle calf stretching"
        ],
        [
            "Small side steps",
            "Chair sit-to-stand",
            "Supported calf raises",
            "Gentle lower-body mobility"
        ]
    ]

    recovery = [
        [
            "Short comfortable walk",
            "Gentle shoulder mobility",
            "Ankle circles",
            "Relaxed breathing"
        ],
        [
            "Slow walking",
            "Gentle stretching",
            "Shoulder relaxation",
            "Quiet recovery time"
        ],
        [
            "Light movement around the room",
            "Gentle arm movements",
            "Ankle mobility",
            "Relaxation and rest"
        ]
    ]

    # Random selection makes each generated plan slightly different
    selected_full = random.choice(full_body)
    selected_upper = random.choice(upper_body)
    selected_lower = random.choice(lower_body)
    selected_recovery = random.choice(recovery)

    selected_warmups = random.choice(warmups)

    # --------------------------------------------------------
    # Goal-specific focus
    # --------------------------------------------------------

    if goal.lower() == "strength":
        goal_focus = """
Your selected goal is Strength.

FitBuddy will focus on comfortable bodyweight movements,
basic functional strength, posture, controlled movement,
and adequate recovery.

The plan does not require heavy weights or extreme training.
"""

    elif goal.lower() == "endurance":
        goal_focus = """
Your selected goal is Endurance.

FitBuddy will focus on comfortable walking, gradual movement,
simple full-body activities, pacing, and recovery.

The goal is to build a consistent movement habit rather than
forcing long or exhausting sessions.
"""

    elif goal.lower() == "flexibility":
        goal_focus = """
Your selected goal is Flexibility.

FitBuddy will focus on gentle mobility, comfortable stretching,
joint movement, posture, relaxation, and recovery.

Stretching should always remain comfortable and should never
be forced or performed with bouncing movements.
"""

    else:
        goal_focus = """
Your selected goal is General Fitness.

FitBuddy will combine comfortable movement, mobility,
basic strength-oriented activities, walking, recovery,
hydration, balanced nutrition, and healthy daily habits.
"""

    # --------------------------------------------------------
    # Feedback section
    # --------------------------------------------------------

    feedback_section = ""

    if feedback:
        feedback_section = f"""
# USER FEEDBACK USED FOR THIS UPDATED PLAN

The following feedback was provided:

"{escape(str(feedback))}"

FitBuddy has considered this feedback while preparing the
updated routine.

The updated routine keeps the activities comfortable,
general, age-appropriate, and flexible.
"""

    # --------------------------------------------------------
    # Helper for warm-up HTML-independent text
    # --------------------------------------------------------

    warmup_text = "\n".join(
        f"- {item}"
        for item in selected_warmups
    )

    # --------------------------------------------------------
    # Build large detailed plan
    # --------------------------------------------------------

    plan = f"""
# FITBUDDY — PERSONALIZED 7-DAY FITNESS & WELLNESS PLAN

## Welcome, {name}! 🌿

Welcome to FitBuddy.

This personalized seven-day wellness plan has been prepared
based on the information entered into the application.

**User Name:** {name}

**Age:** {age}

**Fitness Goal:** {goal}

**Preferred Intensity:** {intensity}

**Activity Level Used:** {intensity_label}

**Suggested Session Duration:** {session_time}

{goal_focus}

The purpose of this plan is to help create a consistent,
comfortable and balanced wellness routine.

You do not need to complete every activity. You can reduce
the number of repetitions, take longer rests, or stop when
you feel tired or uncomfortable.

{feedback_section}

# WEEKLY PLAN OVERVIEW 📅

## Day 1 — Full Body Movement

Main focus:
- Comfortable full-body movement
- Basic functional exercises
- Mobility
- Recovery

Suggested duration:
{session_time}

## Day 2 — Walking & Mobility

Main focus:
- Comfortable walking
- Flexibility
- Joint mobility
- Relaxation

## Day 3 — Upper Body & Core Stability

Main focus:
- Upper-body movement
- Posture
- Comfortable core stability
- Recovery

## Day 4 — Active Recovery

Main focus:
- Light movement
- Stretching
- Relaxation
- Rest

## Day 5 — Lower Body & Balance

Main focus:
- Comfortable lower-body movement
- Balance
- Functional movement
- Mobility

## Day 6 — Full Body Routine

Main focus:
- Combining familiar movements
- Comfortable activity
- Mobility
- Recovery

## Day 7 — Recovery & Weekly Review

Main focus:
- Rest
- Reflection
- Gentle movement
- Preparing for the next week


# DAY 1 — FULL BODY MOVEMENT 🏃

## Objective

The first day introduces basic movements in a comfortable
and controlled way.

The main purpose is to establish a routine rather than
trying to complete a difficult workout.

## Warm-Up

Spend a few minutes preparing the body.

{warmup_text}

## Main Activities

### 1. Chair Sit-to-Stand

- Use a stable chair.
- Sit down slowly.
- Stand up comfortably.
- Keep the movement controlled.
- Use your hands for support if needed.
- Suggested amount: {repetitions}.
- Rest whenever necessary.

### 2. Wall Push-Ups

- Stand facing a stable wall.
- Place your hands comfortably on the wall.
- Bend your elbows slowly.
- Push yourself gently away from the wall.
- Keep the movement controlled.
- Suggested amount: {repetitions}.

### 3. Standing Calf Raises

- Stand near a stable support.
- Slowly raise your heels.
- Lower your heels gradually.
- Avoid rushing the movement.
- Suggested amount: {repetitions}.

### 4. Comfortable Walking

- Walk at a comfortable pace.
- Keep your breathing natural.
- Choose a safe walking area.
- Suggested duration: 5–10 minutes.

## Recovery

After the activities:

- Walk slowly for a short period.
- Relax your shoulders.
- Take comfortable breaths.
- Drink water according to your normal needs.
- Allow your body to rest.

## Day 1 Reminder

The first day is about starting comfortably.
You do not need to push yourself.


# DAY 2 — WALKING & MOBILITY 🚶

## Objective

Day 2 focuses on comfortable movement and flexibility.

## Warm-Up

- Walk slowly for 2 minutes.
- Perform gentle shoulder rolls.
- Move your wrists.
- Move your ankles gently.

## Main Activities

### Comfortable Walking

- Choose a safe and comfortable place.
- Start slowly.
- Maintain a pace that feels manageable.
- Suggested duration: 5–15 minutes.

### Shoulder Mobility

- Roll the shoulders gently.
- Keep the movement slow.
- Repeat 5–8 times.

### Standing Side Reach

- Stand comfortably.
- Reach one arm gently to the side or overhead.
- Do not force the stretch.
- Change sides.
- Repeat 3–5 times per side.

### Ankle Mobility

- Sit or stand with support.
- Move each ankle gently.
- Repeat several times.

## Recovery

- Sit comfortably after the session.
- Relax your shoulders.
- Take a few natural breaths.
- Drink water normally.
- Continue your regular daily activities.

## Day 2 Reminder

Small amounts of comfortable movement can be part of
a healthy daily routine.


# DAY 3 — UPPER BODY & CORE STABILITY 💪

## Objective

Day 3 introduces simple upper-body and posture-oriented
movements.

## Warm-Up

- Gentle marching.
- Shoulder rolls.
- Arm movements.
- Wrist mobility.

## Main Activities

### 1. Wall Push-Ups

- Keep your hands at a comfortable height.
- Bend your elbows slowly.
- Push away from the wall.
- Suggested amount: {repetitions}.

### 2. Seated Arm Raises

- Sit on a stable chair.
- Raise your arms comfortably.
- Lower them slowly.
- Repeat {repetitions}.

### 3. Seated Knee Extensions

- Sit upright.
- Extend one lower leg comfortably.
- Return to the starting position.
- Change sides.
- Repeat several times.

### 4. Standing Balance

- Stand near a stable support.
- Shift your weight gently.
- Keep your movements controlled.
- Continue only while comfortable.

## Recovery

- Relax your arms.
- Stretch gently.
- Sit down if you feel tired.
- Drink water normally.
- Allow adequate recovery time.

## Day 3 Reminder

Controlled movement is more important than rushing.


# DAY 4 — ACTIVE RECOVERY 🌱

## Objective

Day 4 is intentionally lighter.

Recovery is an important part of a balanced wellness routine.

## Gentle Activities

Choose one or more comfortable options:

- Short walk.
- Gentle stretching.
- Shoulder mobility.
- Ankle mobility.
- Relaxed breathing.
- Quiet rest.

Suggested duration:
5–10 minutes or less if preferred.

## Recovery Checklist

- Take enough rest.
- Eat regular balanced meals.
- Drink water regularly.
- Maintain a comfortable sleep routine.
- Take breaks from long periods of sitting.

## Day 4 Reminder

Rest is not failure.

Recovery gives your body time to relax between active days.


# DAY 5 — LOWER BODY & BALANCE 🦵

## Objective

Day 5 focuses on comfortable lower-body movements.

## Warm-Up

- Gentle marching.
- Ankle circles.
- Shoulder movements.
- Slow walking.

## Main Activities

### 1. Chair Sit-to-Stand

- Use a stable chair.
- Sit and stand slowly.
- Keep the movement controlled.
- Suggested amount: {repetitions}.

### 2. Supported Calf Raises

- Hold a stable support.
- Raise your heels.
- Lower slowly.
- Suggested amount: {repetitions}.

### 3. Side Steps

- Stand near a stable support.
- Take a small step sideways.
- Bring the other foot alongside.
- Change direction.
- Continue for a short comfortable period.

### 4. Gentle Leg Stretch

- Place one foot slightly behind the other.
- Move into a comfortable position.
- Do not bounce.
- Stop if uncomfortable.
- Change sides.

## Recovery

- Walk slowly for a minute.
- Relax your legs.
- Sit if needed.
- Drink water normally.
- Continue with your normal day.

## Day 5 Reminder

Move slowly and keep balance as the priority.


# DAY 6 — FULL BODY ROUTINE 🌟

## Objective

Day 6 combines movements introduced earlier in the week.

## Warm-Up

- Gentle marching.
- Shoulder rolls.
- Arm movements.
- Ankle mobility.

## Main Activities

### 1. Comfortable Walking

Suggested duration:
5–15 minutes.

### 2. Wall Push-Ups

Suggested amount:
{repetitions}.

### 3. Chair Sit-to-Stand

Suggested amount:
{repetitions}.

### 4. Standing Arm Movements

- Raise your arms comfortably.
- Lower them slowly.
- Repeat several times.

### 5. Gentle Stretching

Stretch comfortably:

- Shoulders
- Arms
- Calves
- Legs

Avoid bouncing or forcing the movement.

## Recovery

- Slow down gradually.
- Relax your muscles.
- Drink water normally.
- Give yourself adequate rest.

## Day 6 Reminder

You can choose fewer activities if your energy is lower.


# DAY 7 — RECOVERY & WEEKLY REVIEW 🌿

## Objective

Day 7 focuses on recovery and reflecting on the week.

## Optional Gentle Movement

If comfortable:

- Short walk.
- Shoulder mobility.
- Ankle mobility.
- Gentle stretching.

You can also choose complete rest.

## Weekly Reflection

Think about:

- Which activities felt comfortable?
- Which activities did you enjoy?
- Which activities would you like to repeat?
- Did you allow enough rest?
- Did you take regular movement breaks?
- Did you drink water regularly?
- Did you eat regular balanced meals?
- Did you maintain a comfortable sleep routine?

## Preparing for Next Week

For the following week:

- Continue activities you enjoy.
- Keep rest periods.
- Make only small changes.
- Avoid suddenly increasing activity.
- Listen to your body's comfort signals.

## Day 7 Reminder

A successful wellness routine is one that fits comfortably
into everyday life.


# GENERAL HEALTHY HABITS 🌿

## 💧 Hydration

- Keep water available during the day.
- Drink regularly according to your normal needs.
- Pay attention to thirst.
- Increase attention to hydration during hot conditions.

## 🥗 Balanced Nutrition

Try to include a variety of familiar foods.

A balanced meal can include combinations of:

- Rice, chapati, oats or another grain.
- Dal, beans, eggs or another protein-containing food.
- Vegetables.
- Fruits.
- Curd or another suitable food.

Do not skip meals simply because you are following
a fitness routine.

## 😴 Sleep & Recovery

- Try to maintain a regular sleep schedule.
- Allow enough time for rest.
- Take breaks when studying or using screens.
- Give yourself quiet time before sleeping.

## 🚶 Everyday Movement

- Take comfortable movement breaks.
- Avoid sitting in the same position for very long periods.
- Walk when convenient.
- Choose activities that you enjoy.

## 🧘 Stress Management

Try simple activities such as:

- Listening to music.
- Reading.
- Spending time with family.
- Quiet breathing.
- Prayer or relaxation.
- Taking a short break from screens.


# NUTRITION GUIDANCE 🍎

## Breakfast

Choose a familiar balanced breakfast such as:

- Idli with sambar.
- Dosa with a suitable side.
- Oats with milk or a suitable alternative.
- Eggs with bread if you eat eggs.
- Fruit with another satisfying food.

## Lunch

A balanced lunch may include:

- Rice or another grain.
- Dal, sambar, beans, eggs or another protein source.
- Vegetables.
- Curd or another suitable food.

## Evening

Possible options include:

- Fruit.
- Sundal.
- Roasted chickpeas.
- Nuts if suitable and safe.
- Another regular snack that you enjoy.

## Dinner

Choose a familiar balanced meal.

Try to include:

- A source of energy.
- A protein-containing food.
- Vegetables where available.

There is no single perfect meal for everyone.


# WEEKLY WELLNESS CHECKLIST ✅

At the end of the week, review:

☐ I included comfortable movement.

☐ I allowed myself enough rest.

☐ I drank water regularly.

☐ I ate regular meals.

☐ I took breaks from long periods of sitting.

☐ I tried to maintain a comfortable sleep routine.

☐ I noticed which activities I enjoyed.

☐ I adjusted activities when I felt tired.

☐ I avoided forcing uncomfortable movements.

☐ I learned something about my own wellness routine.


# SAFETY GUIDELINES ⚠️

This is a general wellness plan.

- Activities should remain comfortable.
- Do not force movements.
- Do not exercise through pain.
- Stop if you feel dizzy, unusually breathless, or unwell.
- Take additional rest whenever necessary.
- Use stable furniture and clear spaces for supported exercises.
- Do not suddenly increase exercise volume.
- If you have a health condition, injury, persistent symptoms,
  or concerns about whether exercise is appropriate, speak with
  a qualified healthcare professional.

This application does not diagnose, treat, or prevent medical conditions.


# FITBUDDY WEEKLY SUMMARY 📊

**Name:** {name}

**Age:** {age}

**Goal:** {goal}

**Preferred Intensity:** {intensity}

**Plan Duration:** 7 Days

**Main Focus:**
Comfortable movement + mobility + recovery +
balanced nutrition + hydration + sleep.

## FINAL MESSAGE 💚

Thank you for using FitBuddy, {name}!

The goal is not to make every day difficult.

The goal is to create a comfortable routine that can fit
into everyday life.

Choose activities that feel suitable for you, take enough
rest, eat regular balanced meals, drink water, and listen
to your body's comfort signals.

Keep moving. Keep learning. Keep taking care of yourself. 🌿

FITBUDDY
Your Fitness & Wellness Companion
"""

    return plan


# ============================================================
# FORMAT PLAN
# ============================================================

def format_plan(text):
    lines = text.splitlines()
    output = []
    in_list = False

    for line in lines:
        line = line.strip()

        if not line:
            if in_list:
                output.append("</ul>")
                in_list = False
            continue

        if line.startswith("# "):
            if in_list:
                output.append("</ul>")
                in_list = False

            heading = escape(line[2:].strip())

            output.append(
                f'<div class="plan-main-heading">✨ {heading}</div>'
            )

        elif line.startswith("## "):
            if in_list:
                output.append("</ul>")
                in_list = False

            heading = escape(line[3:].strip())

            output.append(
                f'<div class="plan-heading">📅 {heading}</div>'
            )

        elif line.startswith("### "):
            if in_list:
                output.append("</ul>")
                in_list = False

            heading = escape(line[4:].strip())

            output.append(
                f'<div class="plan-subheading">{heading}</div>'
            )

        elif line.startswith("- "):
            if not in_list:
                output.append('<ul class="plan-list">')
                in_list = True

            item = escape(line[2:].strip())

            output.append(
                f"<li>{item}</li>"
            )

        elif line.startswith("☐ "):
            if not in_list:
                output.append('<ul class="plan-list">')
                in_list = True

            item = escape(line[2:].strip())

            output.append(
                f"<li>☐ {item}</li>"
            )

        else:
            if in_list:
                output.append("</ul>")
                in_list = False

            output.append(
                f'<p class="plan-text">{escape(line)}</p>'
            )

    if in_list:
        output.append("</ul>")

    return "\n".join(output)


# ============================================================
# HOME PAGE
# ============================================================

@app.get("/", response_class=HTMLResponse)
def home():

    return """
<!DOCTYPE html>
<html>
<head>

<title>FitBuddy - AI Fitness Plan Generator</title>

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial, sans-serif;

    background:
        linear-gradient(
            135deg,
            #e8f5e9,
            #e3f2fd
        );

    color: #17324d;
}

.container {
    max-width: 650px;
    margin: 50px auto;
    padding: 20px;
}

.card {
    background: white;
    padding: 35px;
    border-radius: 25px;

    box-shadow:
        0 10px 30px rgba(0,0,0,0.08);
}

.logo {
    text-align: center;
    font-size: 55px;
}

h1 {
    text-align: center;
    margin: 10px 0;
    color: #1b5e20;
}

.subtitle {
    text-align: center;
    color: #607d8b;
    margin-bottom: 30px;
    line-height: 1.6;
}

label {
    display: block;
    margin-top: 18px;
    margin-bottom: 7px;
    font-weight: bold;
}

input,
select {
    width: 100%;
    padding: 13px;

    border:
        1px solid #cfd8dc;

    border-radius: 12px;

    font-size: 15px;

    background: #fafafa;
}

input:focus,
select:focus {
    outline: none;
    border-color: #43a047;
}

button {
    width: 100%;
    margin-top: 28px;
    padding: 15px;

    border: none;
    border-radius: 13px;

    background: #2e7d32;
    color: white;

    font-size: 17px;
    font-weight: bold;

    cursor: pointer;
}

button:hover {
    background: #1b5e20;
}

.note {
    text-align: center;
    margin-top: 20px;
    color: #78909c;
    font-size: 13px;
    line-height: 1.6;
}

</style>

</head>

<body>

<div class="container">

<div class="card">

<div class="logo">
🏃‍♀️💚
</div>

<h1>FitBuddy</h1>

<p class="subtitle">
Personalized Fitness & Wellness Plan Generator
</p>

<form action="/generate-workout"
      method="post">

<label>Name</label>

<input
    type="text"
    name="name"
    placeholder="Enter your name"
    required
>

<label>Age</label>

<input
    type="number"
    name="age"
    min="13"
    max="100"
    placeholder="Enter your age"
    required
>

<label>Fitness Goal</label>

<select name="goal" required>

<option value="">
Select your goal
</option>

<option value="General Fitness">
General Fitness
</option>

<option value="Strength">
Strength
</option>

<option value="Endurance">
Endurance
</option>

<option value="Flexibility">
Flexibility
</option>

</select>

<label>Preferred Intensity</label>

<select name="intensity" required>

<option value="">
Select intensity
</option>

<option value="Low">
Low
</option>

<option value="Moderate">
Moderate
</option>

<option value="High">
High
</option>

</select>

<button type="submit">
✨ Generate My Plan
</button>

</form>

<p class="note">
🌿 FitBuddy creates a detailed wellness plan locally.
<br>
No API key is required.
</p>

</div>

</div>

</body>
</html>
"""


# ============================================================
# GENERATE WORKOUT
# ============================================================

@app.post(
    "/generate-workout",
    response_class=HTMLResponse
)
def generate_workout(
    name: str = Form(...),
    age: int = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...)
):

    plan = generate_local_plan(
        name=name,
        age=age,
        goal=goal,
        intensity=intensity
    )

    # --------------------------------------------------------
    # Save to database
    # --------------------------------------------------------

    try:

        db = SessionLocal()

        new_plan = FitnessPlan(
            name=name,
            age=age,
            goal=goal,
            intensity=intensity,
            plan=plan
        )

        db.add(new_plan)
        db.commit()

        db.close()

    except Exception:
        pass

    formatted_plan = format_plan(plan)

    safe_name = escape(name)
    safe_goal = escape(goal)
    safe_intensity = escape(intensity)

    return f"""
<!DOCTYPE html>
<html>

<head>

<title>FitBuddy - Your Plan</title>

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<style>

* {{
    box-sizing: border-box;
}}

body {{
    margin: 0;
    font-family: Arial, sans-serif;

    background:
        linear-gradient(
            135deg,
            #e8f5e9,
            #e3f2fd
        );

    color: #17324d;
}}

.page {{
    max-width: 950px;
    margin: auto;
    padding: 25px 15px 50px;
}}

.header {{
    background: white;
    border-radius: 25px;
    padding: 30px;

    text-align: center;

    box-shadow:
        0 8px 25px rgba(0,0,0,0.08);

    margin-bottom: 22px;
}}

.header-icon {{
    font-size: 50px;
}}

.header h1 {{
    margin: 8px 0;
    font-size: 34px;
    color: #1b5e20;
}}

.header p {{
    color: #607d8b;
    font-size: 17px;
}}

.profile {{
    display: grid;
    grid-template-columns:
        repeat(3, 1fr);

    gap: 15px;

    margin-bottom: 22px;
}}

.profile-card {{
    background: white;
    padding: 20px;

    border-radius: 20px;

    text-align: center;

    box-shadow:
        0 6px 20px rgba(0,0,0,0.06);
}}

.profile-icon {{
    font-size: 30px;
    margin-bottom: 8px;
}}

.profile-card small {{
    display: block;
    margin-top: 6px;
    color: #78909c;
}}

.ai-card {{
    background: white;
    border-radius: 25px;

    padding: 30px;

    box-shadow:
        0 8px 25px rgba(0,0,0,0.08);

    margin-bottom: 22px;
}}

.ai-title {{
    font-size: 25px;
    font-weight: bold;

    color: #1b5e20;

    margin-bottom: 22px;
}}

.plan {{
    background: #f8fbff;

    border-radius: 20px;

    padding: 25px;

    border-left:
        6px solid #42a5f5;

    line-height: 1.7;
}}

.plan-main-heading {{
    font-size: 25px;
    font-weight: bold;

    color: #1565c0;

    padding: 15px 0;

    border-bottom:
        1px solid #e3f2fd;

    margin-bottom: 15px;
}}

.plan-heading {{
    font-size: 20px;
    font-weight: bold;

    color: #2e7d32;

    background: #e8f5e9;

    padding: 12px 15px;

    border-radius: 12px;

    margin-top: 20px;
    margin-bottom: 12px;
}}

.plan-subheading {{
    font-size: 18px;
    font-weight: bold;

    color: #455a64;

    margin-top: 15px;
}}

.plan-text {{
    color: #455a64;
    margin: 8px 0;
}}

.plan-list {{
    padding-left: 25px;
}}

.plan-list li {{
    margin: 8px 0;
    color: #455a64;
}}

.feedback-box {{
    background: white;

    border-radius: 25px;

    padding: 28px;

    box-shadow:
        0 8px 25px rgba(0,0,0,0.07);

    margin-bottom: 22px;
}}

.feedback-box h2 {{
    color: #1b5e20;
    margin-top: 0;
}}

.feedback-box p {{
    color: #607d8b;
    line-height: 1.6;
}}

.feedback-box textarea {{
    width: 100%;

    min-height: 130px;

    padding: 15px;

    border:
        1px solid #cfd8dc;

    border-radius: 12px;

    font-size: 15px;

    resize: vertical;

    font-family: Arial, sans-serif;
}}

.feedback-box button {{
    width: 100%;

    margin-top: 15px;

    padding: 15px;

    border: none;

    border-radius: 13px;

    background: #2e7d32;

    color: white;

    font-size: 17px;

    font-weight: bold;

    cursor: pointer;
}}

.button {{
    display: block;

    text-align: center;

    text-decoration: none;

    background: #2e7d32;

    color: white;

    padding: 16px;

    border-radius: 15px;

    font-size: 17px;

    font-weight: bold;
}}

.footer {{
    text-align: center;

    color: #78909c;

    margin-top: 25px;

    font-size: 14px;
}}

@media (max-width: 650px) {{

    .profile {{
        grid-template-columns: 1fr;
    }}

    .header h1 {{
        font-size: 27px;
    }}

    .ai-card {{
        padding: 20px;
    }}

    .plan {{
        padding: 18px;
    }}

}}

</style>

</head>

<body>

<div class="page">

<div class="header">

<div class="header-icon">
🏃‍♀️💚
</div>

<h1>FitBuddy</h1>

<p>
Your Personalized Fitness & Wellness Companion
</p>

</div>


<div class="profile">

<div class="profile-card">

<div class="profile-icon">
👤
</div>

<b>{safe_name}</b>

<small>
Name
</small>

</div>


<div class="profile-card">

<div class="profile-icon">
🎯
</div>

<b>{safe_goal}</b>

<small>
Fitness Goal
</small>

</div>


<div class="profile-card">

<div class="profile-icon">
⚡
</div>

<b>{safe_intensity}</b>

<small>
Preferred Intensity
</small>

</div>

</div>


<div class="ai-card">

<div class="ai-title">
🤖 FitBuddy Generated 7-Day Plan
</div>

<div class="plan">

{formatted_plan}

</div>

</div>


<div class="feedback-box">

<h2>
🔄 Improve Your Plan
</h2>

<p>
Have any suggestions for your plan?
Tell FitBuddy what you would like to change.
</p>

<form action="/submit-feedback"
      method="post">

<input
    type="hidden"
    name="name"
    value="{safe_name}"
>

<input
    type="hidden"
    name="age"
    value="{age}"
>

<input
    type="hidden"
    name="goal"
    value="{safe_goal}"
>

<input
    type="hidden"
    name="intensity"
    value="{safe_intensity}"
>

<input
    type="hidden"
    name="original_plan"
    value="{escape(plan)}"
>

<textarea
    name="feedback"
    placeholder="Example: Make the activities easier and include more rest."
    required
></textarea>

<button type="submit">
🔄 Update My Plan
</button>

</form>

</div>


<a class="button" href="/">
✨ Create Another Plan
</a>


<div class="footer">

FitBuddy • Local Personalized Wellness Generator 🌿

</div>

</div>

</body>

</html>
"""


# ============================================================
# FEEDBACK / UPDATE PLAN
# ============================================================

@app.post(
    "/submit-feedback",
    response_class=HTMLResponse
)
def submit_feedback(
    name: str = Form(...),
    age: int = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
    original_plan: str = Form(...),
    feedback: str = Form(...)
):

    updated_plan = generate_local_plan(
        name=name,
        age=age,
        goal=goal,
        intensity=intensity,
        feedback=feedback
    )

    # Save updated plan
    try:

        db = SessionLocal()

        new_plan = FitnessPlan(
            name=name,
            age=age,
            goal=goal,
            intensity=intensity,
            plan=updated_plan
        )

        db.add(new_plan)
        db.commit()

        db.close()

    except Exception:
        pass

    formatted_plan = format_plan(updated_plan)

    return f"""
<!DOCTYPE html>

<html>

<head>

<title>FitBuddy - Updated Plan</title>

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<style>

body {{
    margin: 0;

    font-family: Arial, sans-serif;

    background:
        linear-gradient(
            135deg,
            #e8f5e9,
            #e3f2fd
        );

    color: #17324d;
}}

.page {{
    max-width: 950px;

    margin: auto;

    padding: 30px 15px 50px;
}}

.card {{
    background: white;

    border-radius: 25px;

    padding: 30px;

    box-shadow:
        0 8px 25px rgba(0,0,0,0.08);

    margin-bottom: 22px;
}}

h1 {{
    color: #1b5e20;
}}

.plan {{
    background: #f8fbff;

    padding: 25px;

    border-radius: 20px;

    border-left:
        6px solid #42a5f5;

    line-height: 1.7;
}}

.plan-main-heading {{
    font-size: 25px;

    font-weight: bold;

    color: #1565c0;

    padding: 15px 0;
}}

.plan-heading {{
    font-size: 20px;

    font-weight: bold;

    color: #2e7d32;

    background: #e8f5e9;

    padding: 12px;

    border-radius: 12px;

    margin-top: 20px;
}}

.plan-subheading {{
    font-size: 18px;

    font-weight: bold;

    color: #455a64;

    margin-top: 15px;
}}

.plan-text {{
    color: #455a64;
}}

.plan-list {{
    padding-left: 25px;
}}

.plan-list li {{
    margin: 8px 0;
}}

.button {{
    display: block;

    text-align: center;

    text-decoration: none;

    background: #2e7d32;

    color: white;

    padding: 16px;

    border-radius: 15px;

    font-weight: bold;
}}

</style>

</head>

<body>

<div class="page">

<div class="card">

<h1>
🔄 Updated FitBuddy Plan
</h1>

<p>
Your plan has been updated based on your feedback.
</p>

</div>


<div class="card">

<div class="plan">

{formatted_plan}

</div>

</div>


<a class="button" href="/">
✨ Create Another Plan
</a>

</div>

</body>

</html>
"""