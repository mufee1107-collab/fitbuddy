from google import genai
from google.genai import types

from .ai_models import WORKOUT_SCHEMA
from .config import settings
from .schemas import (
    UserInput,
    WorkoutPlan
)


def get_client():

    if not settings.gemini_api_key:

        raise RuntimeError(
            "GEMINI_API_KEY is not configured."
        )

    return genai.Client(
        api_key=settings.gemini_api_key
    )


def generate_mock_workout(
    data: UserInput
):

    focus_by_goal = {

        "weight_loss":
            "Cardio + Full Body",

        "muscle_gain":
            "Strength + Full Body",

        "general_wellness":
            "Balanced Full Body",

        "flexibility":
            "Mobility + Flexibility"
    }

    days = []

    for i in range(1, 8):

        if i in (3, 7):

            focus = "Recovery / Mobility"

        else:

            focus = focus_by_goal[
                data.goal
            ]

        days.append({

            "day": f"Day {i}",

            "focus": focus,

            "warm_up": [
                "5 minutes of easy movement",
                "Gentle dynamic mobility"
            ],

            "exercises": [

                {
                    "name":
                        "Bodyweight Squat",

                    "sets":
                        2,

                    "reps_or_duration":
                        "8–12 reps",

                    "rest":
                        "60–90 seconds",

                    "notes":
                        "Use a comfortable range of motion."
                },

                {
                    "name":
                        "Wall Push-up",

                    "sets":
                        2,

                    "reps_or_duration":
                        "8–12 reps",

                    "rest":
                        "60–90 seconds",

                    "notes":
                        "Keep the movement controlled."
                },

                {
                    "name":
                        "Easy Walk",

                    "sets":
                        1,

                    "reps_or_duration":
                        "10–15 minutes",

                    "rest":
                        "As needed",

                    "notes":
                        "Keep the pace comfortable."
                }
            ],

            "cool_down": [
                "Gentle stretching",
                "Slow breathing for a few minutes"
            ]
        })

    return WorkoutPlan(

        title=(
            "FitBuddy 7-Day "
            +
            data.goal
            .replace("_", " ")
            .title()
            +
            " Plan"
        ),

        overview=(
            "A general wellness template designed "
            "around consistency, comfortable effort, "
            "recovery, and gradual progress."
        ),

        safety_note=(
            "Stop if you feel pain, dizziness, "
            "or feel unwell. For health conditions "
            "or individualized exercise advice, "
            "consult a qualified professional."
        ),

        days=days
    )


def generate_workout_gemini(
    data: UserInput
):

    if settings.use_mock_ai:

        return generate_mock_workout(
            data
        )

    prompt = f"""

You are FitBuddy, a conservative
wellness-planning assistant.

Create a safe, age-appropriate,
general 7-day activity plan using:

Name: {data.name}

Age: {data.age}

Weight: {data.weight} kg

Goal: {data.goal}

Intensity: {data.intensity}

Requirements:

1. Return exactly 7 days.

2. Include a warm-up.

3. Include main exercises.

4. Include cooldown or recovery.

5. Match the requested intensity.

6. Avoid extreme exercise.

7. Do not recommend extreme calorie restriction.

8. Do not recommend fasting.

9. Do not recommend supplements.

10. Do not diagnose medical conditions.

11. Provide practical sets,
repetitions/duration and rest.

12. Include a concise safety note.

13. Return ONLY JSON matching
the supplied schema.

"""

    client = get_client()

    response = client.models.generate_content(

        model=settings.gemini_workout_model,

        contents=prompt,

        config=types.GenerateContentConfig(

            response_mime_type="application/json",

            response_schema=WORKOUT_SCHEMA
        )
    )

    if not response.text:

        raise RuntimeError(
            "Gemini returned an empty workout response."
        )

    return WorkoutPlan.model_validate_json(
        response.text
    )