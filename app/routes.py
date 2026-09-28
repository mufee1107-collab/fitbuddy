import json

from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    Request
)

from fastapi.responses import (
    HTMLResponse,
    RedirectResponse
)

from fastapi.templating import (
    Jinja2Templates
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
    delete_user,
    get_all_users,
    get_plan,
    save_plan,
    save_user,
    update_plan
)

from .schemas import (
    FeedbackRequest,
    UserInput,
    WorkoutPlan,
    NutritionTip
)

from .security import require_admin

from .updated_plan import (
    update_workout_plan
)

from .models import User


router = APIRouter()


templates = Jinja2Templates(
    directory="app/templates"
)


def plan_to_json(
    plan: WorkoutPlan
):

    return json.dumps(
        plan.model_dump(),
        ensure_ascii=False,
        indent=2
    )


def render_error(
    request: Request,
    message: str,
    status_code: int = 500
):

    return templates.TemplateResponse(

        request=request,

        name="error.html",

        context={
            "message": message
        },

        status_code=status_code
    )


@router.get(
    "/",
    response_class=HTMLResponse
)
def home(
    request: Request
):

    return templates.TemplateResponse(

        request=request,

        name="index.html",

        context={}
    )


@router.post(
    "/generate-workout",
    response_class=HTMLResponse
)
def generate_workout(

    request: Request,

    name: str = Form(...),

    user_id: str = Form(...),

    age: int = Form(...),

    weight: float = Form(...),

    goal: str = Form(...),

    intensity: str = Form(...),

    db: Session = Depends(get_db)
):

    try:

        data = UserInput(

            name=name,

            user_id=user_id,

            age=age,

            weight=weight,

            goal=goal,

            intensity=intensity
        )

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

            plan_to_json(
                workout
            ),

            nutrition.model_dump_json()
        )

        return templates.TemplateResponse(

            request=request,

            name="result.html",

            context={

                "user": data,

                "workout": workout,

                "nutrition": nutrition,

                "message":
                    "Your personalized "
                    "7-day plan is ready.",

                "updated": False
            }
        )

    except ValueError as exc:

        return render_error(

            request,

            str(exc),

            422
        )

    except Exception as exc:

        return render_error(

            request,

            str(exc),

            500
        )


@router.post(
    "/submit-feedback",
    response_class=HTMLResponse
)
def submit_feedback(

    request: Request,

    user_id: str = Form(...),

    feedback: str = Form(...),

    db: Session = Depends(get_db)
):

    try:

        feedback_data = FeedbackRequest(

            user_id=user_id,

            feedback=feedback
        )

        plan = get_plan(

            db,

            feedback_data.user_id
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

            feedback_data.feedback
        )

        user = db.query(User).filter(

            User.user_id ==
            feedback_data.user_id

        ).first()

        if not user:

            raise HTTPException(

                status_code=404,

                detail="User not found."
            )

        update_plan(

            db,

            plan,

            plan_to_json(
                updated
            ),

            feedback_data.feedback
        )

        nutrition = (
            NutritionTip
            .model_validate_json(
                plan.nutrition_tip
            )
        )

        return templates.TemplateResponse(

            request=request,

            name="result.html",

            context={

                "user": user,

                "workout": updated,

                "nutrition": nutrition,

                "message":
                    "Your plan was updated "
                    "using your feedback.",

                "updated": True
            }
        )

    except HTTPException as exc:

        return render_error(

            request,

            exc.detail,

            exc.status_code
        )

    except Exception as exc:

        return render_error(

            request,

            str(exc),

            500
        )


@router.get(
    "/view-all-users",
    response_class=HTMLResponse
)
def view_all_users(

    request: Request,

    db: Session = Depends(get_db),

    _: str = Depends(require_admin)
):

    users = get_all_users(db)

    rows = []

    for user in users:

        plan = get_plan(

            db,

            user.user_id
        )

        rows.append({

            "user": user,

            "plan": plan
        })

    return templates.TemplateResponse(

        request=request,

        name="all_users.html",

        context={
            "rows": rows
        }
    )


@router.post(
    "/admin/delete/{user_id}"
)
def admin_delete_user(

    user_id: str,

    db: Session = Depends(get_db),

    _: str = Depends(require_admin)
):

    delete_user(

        db,

        user_id
    )

    return RedirectResponse(

        url="/view-all-users",

        status_code=303
    )


@router.get("/health")
def health():

    return {
        "status": "ok"
    }