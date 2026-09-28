from .schemas import (
    WorkoutPlan,
    NutritionTip
)


WORKOUT_SCHEMA = (
    WorkoutPlan
    .model_json_schema()
)


TIP_SCHEMA = (
    NutritionTip
    .model_json_schema()
)