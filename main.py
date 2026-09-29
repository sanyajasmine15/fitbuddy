import os
from html import escape
from fastapi import FastAPI, Form
from database import SessionLocal, FitnessPlan


from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
from google import genai


# Load API key from .env
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

app = FastAPI(title="FitBuddy - AI Fitness Plan Generator")


# Connect to Gemini
client = genai.Client(api_key=API_KEY) if API_KEY else None

def format_plan(text):
    """
    Convert Gemini's simple Markdown-style response
    into a cleaner HTML display.
    """

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

        # Main heading
        if line.startswith("# "):
            if in_list:
                output.append("</ul>")
                in_list = False

            heading = escape(line[2:].strip())

            output.append(
                f'<div class="plan-main-heading">✨ {heading}</div>'
            )

        # Sub heading
        elif line.startswith("## "):
            if in_list:
                output.append("</ul>")
                in_list = False

            heading = escape(line[3:].strip())

            output.append(
                f'<div class="plan-heading">📅 {heading}</div>'
            )

        # Smaller heading
        elif line.startswith("### "):
            if in_list:
                output.append("</ul>")
                in_list = False

            heading = escape(line[4:].strip())

            output.append(
                f'<div class="plan-subheading">{heading}</div>'
            )

        # Bullet points
        elif line.startswith("- ") or line.startswith("* "):
            if not in_list:
                output.append('<ul class="plan-list">')
                in_list = True

            item = escape(line[2:].strip())
            output.append(f"<li>{item}</li>")

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
                background: linear-gradient(
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
                border: 1px solid #cfd8dc;
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
                    AI-Powered Fitness & Wellness Plan Generator
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
                        ✨ Generate My AI Plan
                    </button>

                </form>

                <p class="note">
                    🤖 Powered by Google Gemini AI
                </p>

            </div>

        </div>

    </body>

    </html>
    """


@app.post("/generate-workout",
          response_class=HTMLResponse)
def generate_workout(
    name: str = Form(...),
    age: int = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...)
):

    prompt = f"""
Create a safe, beginner-friendly 7-day general fitness
and wellness plan.

User name: {name}
Age: {age}
Fitness goal: {goal}
Preferred intensity: {intensity}

Structure the response clearly like this:

# 7-Day Fitness & Wellness Plan

## Day 1
- Activity
- Recovery suggestion

## Day 2
- Activity
- Recovery suggestion

Continue through Day 7.

Then include:

# General Healthy Habits for the Week

- Hydration
- Balanced nutrition
- Comfortable movement
- Rest and recovery
- Stress management

Keep the advice general and safe.

Do not provide restrictive diets,
extreme exercise,
weight-loss targets,
body comparisons,
or medical advice.
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        plan = response.text

        formatted_plan = format_plan(plan)

    except Exception as e:

        formatted_plan = f"""
        <div class="error">
            ⚠️ Gemini API Error
            <br><br>
            {escape(str(e))}
        </div>
        """

    safe_name = escape(name)
    safe_goal = escape(goal)
    safe_intensity = escape(intensity)

    return f"""
    <!DOCTYPE html>

    <html>

    <head>

        <title>FitBuddy AI Plan</title>

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

            .habit {{
                background: white;
                border-radius: 25px;
                padding: 28px;

                box-shadow:
                    0 8px 25px rgba(0,0,0,0.07);

                margin-bottom: 22px;
            }}

            .habit h2 {{
                color: #1b5e20;
                margin-top: 0;
            }}

            .habit-grid {{
                display: grid;
                grid-template-columns:
                    repeat(2, 1fr);

                gap: 15px;
            }}

            .habit-item {{
                padding: 20px;
                border-radius: 17px;
                background: #f8fdf9;

                border:
                    1px solid #e0f2e1;

                line-height: 1.6;
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

                box-shadow:
                    0 5px 15px rgba(46,125,50,0.2);
            }}

            .button:hover {{
                background: #1b5e20;
            }}

            .footer {{
                text-align: center;
                color: #78909c;

                margin-top: 25px;
                font-size: 14px;
            }}

            .error {{
                background: #ffebee;
                color: #c62828;

                padding: 20px;
                border-radius: 15px;
                line-height: 1.6;
            }}

            @media (max-width: 650px) {{

                .profile {{
                    grid-template-columns: 1fr;
                }}

                .habit-grid {{
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
.feedback-box {{
    background: white;
    border-radius: 25px;
    padding: 28px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.07);
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
    min-height: 120px;
    padding: 15px;
    border: 1px solid #cfd8dc;
    border-radius: 12px;
    font-size: 15px;
    resize: vertical;
    font-family: Arial, sans-serif;
}}

.feedback-box textarea:focus {{
    outline: none;
    border-color: #43a047;
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
                    Your AI-Powered Fitness & Wellness Companion
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
                    🤖 Gemini AI Generated Plan
                </div>

                <div class="plan">

                    {formatted_plan}

                </div>

            </div>


            <div class="habit">

                <h2>
                    💡 General Healthy Habits for the Week
                </h2>

                <div class="habit-grid">

                    <div class="habit-item">
                        💧 <b>Stay Hydrated</b><br>
                        Drink water regularly throughout the day.
                    </div>

                    <div class="habit-item">
                        🥗 <b>Balanced Nutrition</b><br>
                        Include a variety of nutritious foods.
                    </div>

                    <div class="habit-item">
                        🚶 <b>Stay Active</b><br>
                        Include comfortable movement and regular breaks.
                    </div>

                    <div class="habit-item">
                        😴 <b>Rest & Recovery</b><br>
                        Give your body enough time to rest and recover.
                    </div>

                </div>

            </div>


            <div class="feedback-box">

    <h2>🔄 Improve Your Plan</h2>

    <p>
        Have any suggestions for your plan?
        Tell FitBuddy what you would like to change.
    </p>

    <form action="/submit-feedback" method="post">

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
                FitBuddy • Powered by Gemini AI 🌿
            </div>

        </div>

    </body>

    </html>
    """
@app.post("/submit-feedback", response_class=HTMLResponse)
def submit_feedback(
    name: str = Form(...),
    age: int = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
    original_plan: str = Form(...),
    feedback: str = Form(...)
):

    prompt = f"""
Update the following 7-day general fitness and wellness plan
based on the user's feedback.

User:
Name: {name}
Age: {age}
Goal: {goal}
Preferred intensity: {intensity}

Original Plan:
{original_plan}

User Feedback:
{feedback}

Create a revised 7-day plan.

Keep the advice safe, beginner-friendly and general.

Do not provide restrictive diets, extreme exercise,
weight-loss targets, body comparisons, or medical advice.

Use this structure:

# Updated 7-Day Fitness & Wellness Plan

## Day 1
- Activity
- Recovery suggestion

Continue through Day 7.

# General Healthy Habits
- Hydration
- Balanced nutrition
- Comfortable movement
- Rest and recovery
- Stress management
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        updated_plan = response.text
        formatted_plan = format_plan(updated_plan)

    except Exception as e:

        formatted_plan = f"""
        <div class="error">
            ⚠️ Gemini API Error
            <br><br>
            {escape(str(e))}
        </div>
        """

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
                background: linear-gradient(
                    135deg,
                    #e8f5e9,
                    #e3f2fd
                );
                color: #17324d;
            }}

            .page {{
                max-width: 950px;
                margin: auto;
                padding: 30px 15px;
            }}

            .card {{
                background: white;
                border-radius: 25px;
                padding: 30px;
                box-shadow: 0 8px 25px rgba(0,0,0,0.08);
                margin-bottom: 22px;
            }}

            h1 {{
                color: #1b5e20;
            }}

            .plan {{
                background: #f8fbff;
                padding: 25px;
                border-radius: 20px;
                border-left: 6px solid #42a5f5;
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

                <h1>🔄 Updated FitBuddy Plan</h1>

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