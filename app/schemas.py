from typing import Literal

from pydantic import (
    BaseModel,
    Field,
    ConfigDict
)


Goal = Literal[
    "weight_loss",
    "muscle_gain",
    "general_wellness",
    "flexibility"
]


Intensity = Literal[
    "low",
    "medium",
    "high"
]


class UserInput(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=120
    )

    user_id: str = Field(
        min_length=2,
        max_length=64,
        pattern=r"^[A-Za-z0-9_-]+$"
    )

    age: int = Field(
        ge=13,
        le=100
    )

    weight: float = Field(
        gt=0,
        le=500
    )

    goal: Goal

    intensity: Intensity


class FeedbackRequest(BaseModel):

    user_id: str = Field(
        min_length=2,
        max_length=64
    )

    feedback: str = Field(
        min_length=3,
        max_length=1000
    )


class Exercise(BaseModel):

    name: str

    sets: int = Field(
        ge=1,
        le=10
    )

    reps_or_duration: str

    rest: str

    notes: str = ""


class DayPlan(BaseModel):

    day: str

    focus: str

    warm_up: list[str]

    exercises: list[Exercise]

    cool_down: list[str]


class WorkoutPlan(BaseModel):

    title: str

    overview: str

    safety_note: str

    days: list[DayPlan] = Field(
        min_length=7,
        max_length=7
    )


class NutritionTip(BaseModel):

    title: str

    tip: str

    hydration: str

    recovery: str


class UserOutput(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    user_id: str

    name: str

    age: int

    weight: float

    goal: str

    intensity: str