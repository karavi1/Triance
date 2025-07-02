import os
import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from src.backend.database.configure import SessionLocal
from src.backend.models.auth_user import AuthUser
from src.backend.models.exercise import Exercise
from src.backend.models.workout import Workout
from src.backend.models.logged_exercise import LoggedExercise, LoggedExerciseSet
from src.backend.models.enums import ExerciseGroup
from src.backend.auth.util import get_password_hash


# -- Exercise data map ------------------------------------------------------
exercise_data = {
    "Push": [
        ("Dips", ["Chest", "Triceps"], ["Shoulders"], "A bodyweight exercise targeting chest & triceps."),
        ("DB Incline Bench", ["Chest"], ["Shoulders", "Triceps"], "Incline dumbbell bench press."),
        ("DB Rear Delts", ["Rear Deltoids"], ["Traps"], "Dumbbell rear delt fly."),
        ("Skullcrushers", ["Triceps"], [], "Lying triceps extension."),
        ("Decline Cable Fly", ["Chest"], ["Shoulders"], "Cable fly on decline bench."),
        ("Leaning Cable Lateral Raises", ["Lateral Deltoids"], ["Traps"], "Leaning cable lateral raise."),
        ("SA Tricep Cable Extension", ["Triceps"], [], "Single-arm cable triceps extension."),
        ("Machine Chest Fly", ["Chest"], ["Shoulders"], "Machine chest fly."),
        ("Machine Rear Delt", ["Rear Deltoids"], ["Mid Back"], "Machine rear delt fly."),
        ("SA Tricep Pushdown", ["Triceps"], [], "Single-arm triceps pushdown."),
    ],
    "Pull": [
        ("Pullups", ["Lats", "Biceps"], ["Forearms"], "Bodyweight pull-up."),
        ("SA Lat Pulldown", ["Lats"], ["Rear Delts"], "Single-arm lat pulldown."),
        ("Incline DB Preachers", ["Biceps"], [], "Incline preacher curl."),
        ("Lat Pullovers", ["Lats"], ["Chest"], "Dumbbell pullover."),
        ("Incline DB Hammers", ["Biceps", "Forearms"], [], "Incline hammer curl."),
        ("DA Cable Rows", ["Mid Back", "Lats"], ["Rear Delts"], "Double-arm cable row."),
        ("Rotator Cuff", ["Rotator Cuff"], [], "Rotator cuff exercise."),
        ("Back and QL Extension", ["Erector Spinae", "Quadratus Lumborum"], [], "Lower back extension."),
    ],
    "Quads": [
        ("DB Squat", ["Quads", "Glutes"], ["Core"], "Dumbbell squat."),
        ("Leg Press", ["Quads", "Glutes"], ["Core", "Hamstrings"], "Leg press machine."),
        ("Seated Calf Raises", ["Calves"], [], "Seated calf raise."),
        ("Weighted Butterflies", ["Adductors"], [], "Weighted hip adduction."),
        ("Cossack Squat", ["Quads", "Adductors"], ["Glutes"], "Side-to-side squat."),
        ("ATG Split Squat", ["Quads"], ["Glutes", "Hamstrings"], "Deep split squat."),
        ("Leg Extensions", ["Quads"], [], "Machine leg extension."),
    ],
    "Hams": [
        ("DB RDL", ["Hamstrings", "Glutes"], ["Lower Back"], "Dumbbell Romanian deadlift."),
        ("Cable Hip Abduction", ["Glute Medius"], [], "Cable hip abduction."),
        ("Reverse Squat/Hip Flexor", ["Hip Flexors"], ["Quads"], "Reverse squat hip flexor."),
        ("Angled Calf Raises", ["Calves"], [], "Angled calf raise."),
        ("Tib Raises", ["Tibialis Anterior"], [], "Tibialis anterior raise."),
        ("Leg Curls", ["Hamstrings"], [], "Machine leg curl."),
    ],
}


def populate_exercises(db: Session):
    with db.begin():
        seen = set()
        for cat_name, items in exercise_data.items():
            try:
                enum_cat = ExerciseGroup(cat_name)            # <<< lookup by value
            except ValueError:
                print(f"⚠ Invalid category '{cat_name}', skipping")
                continue

            for name, primary, secondary, desc in items:
                if name in seen:
                    continue
                seen.add(name)

                exists = db.query(Exercise).filter_by(name=name).first()
                if not exists:
                    ex = Exercise(
                        id=uuid.uuid4(),
                        name=name,
                        category=enum_cat,
                        primary_muscles=primary,
                        secondary_muscles=secondary or None,
                        description=desc,
                    )
                    db.add(ex)
                    print(f"➕ Added exercise: {name} [{enum_cat.value}]")
                else:
                    print(f"✔️  Already have exercise: {name}")


# -- Sample users + workouts ------------------------------------------------
sample_users = [
    {
        "username": "bob",
        "email": "bob@gmail.com",
        "password": "secret123",
        "workouts": [
            {
                "notes": "Push Day - Chest & Triceps focus",
                "days_ago": 4,
                "type": "Push",
                "logged_exercises": [
                    ("DB Incline Bench", 4, 10, 32.5),
                    ("Dips", 3, 12, 0),
                    ("SA Tricep Cable Extension", 3, 15, 10),
                    ("Leaning Cable Lateral Raises", 3, 12, 7.5),
                ],
            },
            {
                "notes": "Leg Day - Quads",
                "days_ago": 2,
                "type": "Quads",
                "logged_exercises": [
                    ("DB Squat", 4, 10, 35),
                    ("Leg Extensions", 4, 12, 45),
                    ("ATG Split Squat", 3, 8, 25),
                    ("Seated Calf Raises", 3, 15, 30),
                ],
            },
        ],
    },
    {
        "username": "jess",
        "email": "jess@example.com",
        "password": "something456",
        "workouts": [
            {
                "notes": "Pull Day - Back & Arms",
                "days_ago": 3,
                "type": "Pull",
                "logged_exercises": [
                    ("Pullups", 3, 8, 0),
                    ("Incline DB Hammers", 3, 10, 15),
                    ("DA Cable Rows", 4, 12, 40),
                    ("Lat Pullovers", 3, 10, 20),
                ],
            },
            {
                "notes": "Leg Day - Hams & Glutes",
                "days_ago": 1,
                "type": "Hams",
                "logged_exercises": [
                    ("DB RDL", 4, 10, 40),
                    ("Leg Curls", 4, 12, 35),
                    ("Cable Hip Abduction", 3, 15, 7.5),
                    ("Tib Raises", 3, 20, 10),
                ],
            },
        ],
    },
    {
        "username": "alfred",
        "email": "alfred@gmail.com",
        "password": "wow789",
        "workouts": [
            {
                "notes": "Push Day - Strength",
                "days_ago": 5,
                "type": "Push",
                "logged_exercises": [
                    ("Dips", 4, 10, 10),
                    ("Skullcrushers", 3, 12, 20),
                    ("Decline Cable Fly", 3, 12, 15),
                ],
            },
            {
                "notes": "Pull + Rotator Rehab",
                "days_ago": 2,
                "type": "Pull",
                "logged_exercises": [
                    ("SA Lat Pulldown", 3, 10, 35),
                    ("Rotator Cuff", 3, 20, 2.5),
                    ("Incline DB Preachers", 3, 10, 12.5),
                ],
            },
        ],
    },
]


def seed_users_and_workouts(db: Session):
    with db.begin():
        for udata in sample_users:
            user = db.query(AuthUser).filter_by(username=udata["username"]).first()
            if not user:
                user = AuthUser(
                    id=uuid.uuid4(),
                    username=udata["username"],
                    email=udata["email"],
                    hashed_password=get_password_hash(udata["password"]),
                )
                db.add(user)
                db.flush()
                print(f"➕ Created user: {user.username}")
            else:
                print(f"✔️  User exists: {user.username}")

            for wdata in udata["workouts"]:
                created_time = datetime.now(timezone.utc) - timedelta(days=wdata["days_ago"])
                enum_type = ExerciseGroup(wdata["type"])   # <<< lookup by value

                workout = (
                    db.query(Workout)
                      .filter_by(user_id=user.id, notes=wdata["notes"], created_time=created_time)
                      .first()
                )
                if not workout:
                    workout = Workout(
                        id=uuid.uuid4(),
                        user_id=user.id,
                        notes=wdata["notes"],
                        created_time=created_time,
                        workout_type=enum_type,
                    )
                    db.add(workout)
                    db.flush()
                    print(f"➕ Seeded workout '{workout.notes}' for {user.username}")
                else:
                    print(f"✔️  Workout exists: {workout.notes}")

                for name, sets_count, reps, weight in wdata["logged_exercises"]:
                    ex = db.query(Exercise).filter_by(name=name).first()
                    if not ex:
                        print(f"⚠ Missing exercise '{name}', skipping")
                        continue

                    le = LoggedExercise(
                        id=uuid.uuid4(),
                        workout_id=workout.id,
                        exercise_id=ex.id,
                    )
                    db.add(le)
                    db.flush()

                    for i in range(sets_count):
                        les = LoggedExerciseSet(
                            logged_exercise_id=le.id,
                            set_number=i + 1,
                            reps=reps,
                            weight=weight,
                        )
                        db.add(les)
                    print(f"   • Logged {sets_count}×{reps}@{weight} for '{name}'")


def main():
    db = SessionLocal()
    try:
        populate_exercises(db)
        seed_users_and_workouts(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()