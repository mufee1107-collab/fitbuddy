from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from .database import get_db

from .gemini_flash_generator import (
    generate_nutrition_tip_with_flash
)

from .gemini_generator import (
    generate_workout_gemini
)

from .repository import (
    get_plan,
    save_plan,
    save_user,
    update_plan
)

from .schemas import (
    FeedbackRequest,
    UserInput,
    WorkoutPlan
)

from .updated_plan import (
    update_workout_plan
)


router = APIRouter(

    prefix="/api",

    tags=["FitBuddy API"]
)


@router.post(
    "/generate"
)
def api_generate(

    data: UserInput,

    db: Session = Depends(get_db)
):

    workout = (
        generate_workout_gemini(
            data
        )
    )

    nutrition = (
        generate_nutrition_tip_with_flash(
            data.goal
        )
    )

    save_user(
        db,
        data
    )

    save_plan(

        db,

        data.user_id,

        workout.model_dump_json(),

        nutrition.model_dump_json()
    )

    return {

        "user":
            data.model_dump(),

        "workout":
            workout.model_dump(),

        "nutrition":
            nutrition.model_dump()
    }


@router.post(
    "/feedback"
)
def api_feedback(

    data: FeedbackRequest,

    db: Session = Depends(get_db)
):

    plan = get_plan(

        db,

        data.user_id
    )

    if not plan:

        raise HTTPException(

            status_code=404,

            detail=
                "No plan found for this User ID."
        )

    original = (
        WorkoutPlan
        .model_validate_json(
            plan.original_plan
        )
    )

    updated = update_workout_plan(

        original,

        data.feedback
    )

    update_plan(

        db,

        plan,

        updated.model_dump_json(),

        data.feedback
    )

    return {

        "user_id":
            data.user_id,

        "updated_workout":
            updated.model_dump(),

        "feedback":
            data.feedback
    }