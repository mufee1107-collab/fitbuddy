from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import User, Plan


def save_user(
    db: Session,
    data
):

    user = db.scalar(
        select(User).where(
            User.user_id == data.user_id
        )
    )

    if user is None:

        user = User(
            user_id=data.user_id,
            name=data.name.strip(),
            age=data.age,
            weight=data.weight,
            goal=data.goal,
            intensity=data.intensity,
        )

        db.add(user)

    else:

        user.name = data.name.strip()
        user.age = data.age
        user.weight = data.weight
        user.goal = data.goal
        user.intensity = data.intensity

    db.commit()

    db.refresh(user)

    return user


def save_plan(
    db: Session,
    user_id: str,
    original_plan: str,
    nutrition_tip: str
):

    plan = Plan(
        user_id=user_id,
        original_plan=original_plan,
        nutrition_tip=nutrition_tip
    )

    db.add(plan)

    db.commit()

    db.refresh(plan)

    return plan


def get_plan(
    db: Session,
    user_id: str
):

    return db.scalar(
        select(Plan)
        .where(
            Plan.user_id == user_id
        )
        .order_by(
            Plan.created_at.desc()
        )
    )


def update_plan(
    db: Session,
    plan: Plan,
    updated_plan: str,
    feedback: str,
    nutrition_tip: str | None = None
):

    plan.updated_plan = updated_plan

    plan.last_feedback = feedback

    if nutrition_tip:

        plan.nutrition_tip = nutrition_tip

    db.commit()

    db.refresh(plan)

    return plan


def get_all_users(
    db: Session
):

    return db.scalars(
        select(User)
        .order_by(
            User.created_at.desc()
        )
    ).all()


def delete_user(
    db: Session,
    user_id: str
):

    user = db.scalar(
        select(User).where(
            User.user_id == user_id
        )
    )

    if not user:

        return False

    plans = db.scalars(
        select(Plan).where(
            Plan.user_id == user_id
        )
    ).all()

    for plan in plans:

        db.delete(plan)

    db.delete(user)

    db.commit()

    return True