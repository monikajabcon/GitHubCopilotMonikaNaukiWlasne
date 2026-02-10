"""
High School Management System API
A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(current_dir, "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Competitive basketball training and games",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["james@mergington.edu"]
    },
    "Tennis Club": {
        "description": "Tennis lessons and match participation",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:00 PM",
        "max_participants": 10,
        "participants": ["ava@mergington.edu"]
    },
    "Drama Club": {
        "description": "Theater productions and acting workshops",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 25,
        "participants": ["isabella@mergington.edu", "lucas@mergington.edu"]
    },
    "Art Class": {
        "description": "Painting, drawing, and sculpture techniques",
        "schedule": "Fridays, 3:30 PM - 4:30 PM",
        "max_participants": 18,
        "participants": ["grace@mergington.edu"]
    },
    "Debate Team": {
        "description": "Competitive debate and public speaking skills",
        "schedule": "Mondays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 16,
        "participants": ["alexander@mergington.edu", "mia@mergington.edu"]
    },
    "Science Club": {
        "description": "Explore science experiments and research projects",
        "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["noah@mergington.edu"]
    }
}

@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")

@app.get("/activities")
def get_activities():
    return activities

@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]

    # Check if activity is full
    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(status_code=400, detail="Activity is at maximum capacity")

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")

    # Add student
    activity["participants"].append(email)
    return {"message": f"Successfully signed up {email} for {activity_name}"}