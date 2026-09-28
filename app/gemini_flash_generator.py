from google import genai
from google.genai import types

from .ai_models import TIP_SCHEMA
from .config import settings
from .schemas import NutritionTip


def get_client():

    if not settings.gemini_api_key:

        raise RuntimeError(
            "GEMINI_API_KEY is not configured."
        )

    return genai.Client(
        api_key=settings.gemini_api_key
    )


def generate_mock_tip(
    goal: str
):

    return NutritionTip(

        title="Balanced Nutrition & Recovery",

        tip=(
            "Build regular meals around a variety "
            "of foods, including protein-rich foods, "
            "whole grains or other carbohydrate "
            "sources, fruits or vegetables, and "
            "healthy fats."
        ),

        hydration=(
            "Drink fluids regularly and respond "
            "to thirst, especially around activity."
        ),

        recovery=(
            "Prioritize regular sleep and rest days "
            "rather than trying to compensate with "
            "extra exercise."
        )
    )


def generate_nutrition_tip_with_flash(
    goal: str
):

    if settings.use_mock_ai:

        return generate_mock_tip(
            goal
        )

    prompt = f"""

Create one concise, practical nutrition
and recovery tip for a FitBuddy user
whose fitness goal is:

{goal}

Requirements:

- Encourage balanced meals.
- Encourage hydration.
- Encourage sleep and recovery.
- Avoid calorie prescriptions.
- Avoid restrictive diets.
- Avoid fasting.
- Avoid supplements.
- Avoid promises of rapid body changes.

Return only JSON matching
the supplied schema.

"""

    client = get_client()

    response = client.models.generate_content(

        model=settings.gemini_tip_model,

        contents=prompt,

        config=types.GenerateContentConfig(

            response_mime_type="application/json",

            response_schema=TIP_SCHEMA
        )
    )

    if not response.text:

        raise RuntimeError(
            "Gemini returned an empty nutrition response."
        )

    return NutritionTip.model_validate_json(
        response.text
    )