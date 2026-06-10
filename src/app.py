"""
High School Management System API

A FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
Now with persistent database storage!
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import os
from pathlib import Path

from database import init_db, get_db
from models import Activity, Participant

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Initialize database
init_db()

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# Sample data to seed database if empty
SAMPLE_ACTIVITIES = [
    {
        "name": "Chess Club",
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
    },
    {
        "name": "Programming Class",
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
    },
    {
        "name": "Gym Class",
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
    },
    {
        "name": "Soccer Team",
        "description": "Join the school soccer team and compete in matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
    },
    {
        "name": "Basketball Team",
        "description": "Practice and play basketball with the school team",
        "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
    },
    {
        "name": "Art Club",
        "description": "Explore your creativity through painting and drawing",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
    },
    {
        "name": "Drama Club",
        "description": "Act, direct, and produce plays and performances",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
    },
    {
        "name": "Math Club",
        "description": "Solve challenging problems and participate in math competitions",
        "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
        "max_participants": 10,
    },
    {
        "name": "Debate Team",
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 12,
    },
]

SAMPLE_PARTICIPANTS = [
    ("Chess Club", "michael@mergington.edu"),
    ("Chess Club", "daniel@mergington.edu"),
    ("Programming Class", "emma@mergington.edu"),
    ("Programming Class", "sophia@mergington.edu"),
    ("Gym Class", "john@mergington.edu"),
    ("Gym Class", "olivia@mergington.edu"),
    ("Soccer Team", "liam@mergington.edu"),
    ("Soccer Team", "noah@mergington.edu"),
    ("Basketball Team", "ava@mergington.edu"),
    ("Basketball Team", "mia@mergington.edu"),
    ("Art Club", "amelia@mergington.edu"),
    ("Art Club", "harper@mergington.edu"),
    ("Drama Club", "ella@mergington.edu"),
    ("Drama Club", "scarlett@mergington.edu"),
    ("Math Club", "james@mergington.edu"),
    ("Math Club", "benjamin@mergington.edu"),
    ("Debate Team", "charlotte@mergington.edu"),
    ("Debate Team", "henry@mergington.edu"),
]


def seed_database(db: Session):
    """Seed database with sample data if empty."""
    if db.query(Activity).count() == 0:
        for activity_data in SAMPLE_ACTIVITIES:
            activity = Activity(**activity_data)
            db.add(activity)
        db.commit()

        for activity_name, email in SAMPLE_PARTICIPANTS:
            activity = db.query(Activity).filter(
                Activity.name == activity_name
            ).first()
            if activity:
                participant = Participant(activity_id=activity.id, email=email)
                db.add(participant)
        db.commit()


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities(db: Session = Depends(get_db)):
    """Get all activities with participant count."""
    seed_database(db)
    activities_data = []
    for activity in db.query(Activity).all():
        participants = db.query(Participant).filter(
            Participant.activity_id == activity.id
        ).all()
        activity_dict = activity.to_dict()
        activity_dict["participants"] = [p.email for p in participants]
        activities_data.append(activity_dict)
    
    result = {}
    for activity in activities_data:
        result[activity.pop("name")] = activity
    return result


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str, db: Session = Depends(get_db)):
    """Sign up a student for an activity."""
    # Find activity by name
    activity = db.query(Activity).filter(Activity.name == activity_name).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Check if student is already signed up
    existing = db.query(Participant).filter(
        Participant.activity_id == activity.id,
        Participant.email == email
    ).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Student is already signed up"
        )

    # Check capacity
    participant_count = db.query(Participant).filter(
        Participant.activity_id == activity.id
    ).count()
    if participant_count >= activity.max_participants:
        raise HTTPException(
            status_code=400,
            detail="Activity is at max capacity"
        )

    # Add student
    participant = Participant(activity_id=activity.id, email=email)
    db.add(participant)
    db.commit()
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str, db: Session = Depends(get_db)):
    """Unregister a student from an activity."""
    # Find activity by name
    activity = db.query(Activity).filter(Activity.name == activity_name).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Find and remove student
    participant = db.query(Participant).filter(
        Participant.activity_id == activity.id,
        Participant.email == email
    ).first()
    if not participant:
        raise HTTPException(
            status_code=400,
            detail="Student is not signed up for this activity"
        )

    # Remove student
    db.delete(participant)
    db.commit()
    return {"message": f"Unregistered {email} from {activity_name}"}
