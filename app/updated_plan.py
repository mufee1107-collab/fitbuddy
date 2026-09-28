from google import genai
from google.genai import types

from .ai_models import WORKOUT_SCHEMA
from .config import settings
from .schemas import WorkoutPlan


def update_workout_plan(
    original_plan: WorkoutPlan,
    feedback: str
):

    if settings.use_mock_ai:

        updated = (
            original_plan
            .model_copy(
                deep=True
            )
        )

        updated.overview = (
            updated.overview
            +
            f" Update requested: {feedback}"
        )

        return updated

    if not settings.gemini_api_key:

        raise RuntimeError(
            "GEMINI_API_KEY is not configured."
        )

    prompt = f"""

You are updating a FitBuddy
7-day wellness plan.

Original plan:

{original_plan.model_dump_json(indent=2)}

User feedback:

{feedback}

Requirements:

1. Apply the user's feedback.

2. Keep exactly 7 days.

3. Maintain safe and sustainable activity.

4. Do not introduce extreme exercise.

5. Do not introduce restrictive eating.

6. Do not introduce fasting.

7. Do not recommend supplements.

8. Do not make medical diagnoses.

9. Return ONLY JSON matching
the supplied schema.

"""

    client = genai.Client(
        api_key=settings.gemini_api_key
    )

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
            "Gemini returned an empty updated plan."
        )

    return WorkoutPlan.model_validate_json(
        response.text
    )