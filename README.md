# FitBuddy – AI Fitness Plan Generator

FitBuddy is an AI-powered fitness and wellness plan generator built using:

- FastAPI
- Python
- Gemini AI
- SQLAlchemy
- SQLite
- Jinja2
- HTML
- CSS

## Features

1. User registration
2. Personalized 7-day workout plan
3. Fitness goals
4. Workout intensity selection
5. AI-generated nutrition/recovery tip
6. Feedback-based plan modification
7. SQLite database
8. Admin dashboard
9. REST API
10. Swagger documentation

## Installation

Create a virtual environment:

python -m venv .venv

Windows:

.venv\Scripts\activate

Install packages:

pip install -r requirements.txt

Create `.env`.

Add:

GEMINI_API_KEY=your_api_key

Run:

uvicorn app.main:app --reload

Open:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs

Admin:

http://127.0.0.1:8000/view-all-users

## Testing

pytest -q

## Mock AI

For testing without Gemini:

USE_MOCK_AI=true

Then start the server.

The application will generate demonstration plans without making Gemini API requests.