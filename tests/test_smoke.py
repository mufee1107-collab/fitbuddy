import os

os.environ["USE_MOCK_AI"] = "true"


from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    assert response.json()["status"] == "ok"


def test_home():

    response = client.get(
        "/"
    )

    assert response.status_code == 200

    assert "FitBuddy" in response.text


def test_generate_in_mock_mode():

    response = client.post(

        "/generate-workout",

        data={

            "name":
                "Demo User",

            "user_id":
                "TEST001",

            "age":
                "20",

            "weight":
                "60",

            "goal":
                "general_wellness",

            "intensity":
                "medium"
        }
    )

    assert response.status_code == 200

    assert (
        "Your personalized 7-day plan is ready."
        in response.text
    )