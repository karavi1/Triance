from sqlalchemy.orm import Session
from src.backend.database.configure import SessionLocal
from src.backend.models import User, Exercise, Workout, LoggedExercise
from src.backend.models.enums import WorkoutType
import uuid
from datetime import datetime, timedelta, timezone

# Map of categories to exercises
exercise_data = {
    "Push": [
        ("Dips", ["Chest", "Triceps"], ["Shoulders"],
         "A bodyweight exercise targeting the chest and triceps by lowering and raising the body on parallel bars."),
        ("DB Incline Bench", ["Chest"], ["Shoulders", "Triceps"],
         "An incline bench press using dumbbells to emphasize the upper portion of the chest."),
        ("DB Rear Delts", ["Rear Deltoids"], ["Traps"],
         "An exercise focusing on the rear deltoid muscles using dumbbells."),
        ("Skullcrushers", ["Triceps"], [],
         "An isolation exercise targeting the triceps by lowering a weight towards the forehead."),
        ("Decline Cable Fly", ["Chest"], ["Shoulders"],
         "A cable exercise performed on a decline bench to target the lower chest."),
        ("Leaning Cable Lateral Raises", ["Lateral Deltoids"], ["Traps"],
         "A cable exercise where the body leans to one side to isolate the lateral deltoid."),
        ("SA Tricep Cable Extension", ["Triceps"], [],
         "A single-arm cable exercise isolating the triceps."),
    ],
    "Pull": [
        ("Pullups", ["Lats", "Biceps"], ["Forearms"],
         "A bodyweight exercise where the body is pulled up towards a bar, engaging the lats and biceps."),
        ("SA Lat Pulldown", ["Lats"], ["Rear Delts"],
         "A single-arm cable exercise pulling a weight down towards the shoulder to target the lats."),
        ("Incline DB Preachers", ["Biceps"], [],
         "An incline bench bicep curl performed with dumbbells."),
        ("Lat Pullovers", ["Lats"], ["Chest"],
         "An exercise where a weight is moved in an arc over the head to target the lats."),
        ("Incline DB Hammers", ["Biceps", "Forearms"], [],
         "An incline bench hammer curl performed with dumbbells."),
        ("DA Cable Rows", ["Mid Back", "Lats"], ["Rear Delts"],
         "A double-arm cable row targeting the mid-back and lats."),
        ("Rotator Cuff", ["Rotator Cuff"], [],
         "Exercises designed to strengthen the rotator cuff muscles."),
        ("Back and QL Extension", ["Erector Spinae", "Quadratus Lumborum"], [],
         "An exercise targeting the lower back and quadratus lumborum muscles."),
    ],
    "Quads": [
        ("DB Squat", ["Quads", "Glutes"], ["Core"],
         "A squat performed with dumbbells to target the quadriceps and glutes."),
        ("Seated Calf Raises", ["Calves"], [],
         "An exercise performed seated to target the calf muscles."),
        ("Weighted butterflies", ["Adductors"], [],
         "An exercise targeting the inner thigh muscles using added weight."),
        ("Cossack Squat", ["Quads", "Adductors"], ["Glutes"],
         "A side-to-side squat movement targeting the quads and adductors."),
        ("Atg Split Squat", ["Quads"], ["Glutes", "Hamstrings"],
         "A deep split squat emphasizing the quadriceps."),
        ("Leg Extensions", ["Quads"], [],
         "An isolation exercise targeting the quadriceps using a machine."),
    ],
    "Hams": [
        ("DB RDL", ["Hamstrings", "Glutes"], ["Lower Back"],
         "A Romanian deadlift performed with dumbbells to target the hamstrings and glutes."),
        ("Cable Hip Abduction", ["Glute Medius"], [],
         "A cable exercise moving the leg away from the body's midline to target the glute medius."),
        ("Reverse squat/Hip Flexor", ["Hip Flexors"], ["Quads"],
         "An exercise targeting the hip flexors and quadriceps."),
        ("Angled Calf Raises", ["Calves"], [],
         "Calf raises performed on an angled platform to target the calf muscles."),
        ("Tib Raises", ["Tibialis Anterior"], [],
         "An exercise targeting the front of the lower leg."),
        ("Leg Curls", ["Hamstrings"], [],
         "An isolation exercise targeting the hamstrings using a machine."),
    ],
}

# Updated sample users and workouts
sample_users = [
    {
        "username": "kaushik",
        "email": "kaush.ravi@gmail.com",
        "workouts": [
            {
                "notes": "Push Day - Chest & Triceps focus",
                "created_time": datetime.now(timezone.utc) - timedelta(days=4),
                "logged_exercises": [
                    ("DB Incline Bench", 4, 10, 32.5),
                    ("Dips", 3, 12, 0),
                    ("SA Tricep Cable Extension", 3, 15, 10),
                    ("Leaning Cable Lateral Raises", 3, 12, 7.5)
                ],
                "workout_type": "Push"
            },
            {
                "notes": "Leg Day - Quads",
                "created_time": datetime.now(timezone.utc) - timedelta(days=2),
                "logged_exercises": [
                    ("DB Squat", 4, 10, 35),
                    ("Leg Extensions", 4, 12, 45),
                    ("Atg Split Squat", 3, 8, 25),
                    ("Seated Calf Raises", 3, 15, 30)
                ],
                "workout_type": "Quads"
            }
        ]
    },
    {
        "username": "jane",
        "email": "jane@example.com",
        "workouts": [
            {
                "notes": "Pull Day - Back & Arms",
                "created_time": datetime.now(timezone.utc) - timedelta(days=3),
                "logged_exercises": [
                    ("Pullups", 3, 8, 0),
                    ("Incline DB Hammers", 3, 10, 15),
                    ("DA Cable Rows", 4, 12, 40),
                    ("Lat Pullovers", 3, 10, 20)
                ],
                "workout_type": "Pull"
            },
            {
                "notes": "Leg Day - Hams & Glutes",
                "created_time": datetime.now(timezone.utc) - timedelta(days=1),
                "logged_exercises": [
                    ("DB RDL", 4, 10, 40),
                    ("Leg Curls", 4, 12, 35),
                    ("Cable Hip Abduction", 3, 15, 7.5),
                    ("Tib Raises", 3, 20, 10)
                ],
                "workout_type": "Hams"
            }
        ]
    },
    {
        "username": "arjun",
        "email": "arjun@example.com",
        "workouts": [
            {
                "notes": "Push Day - Strength",
                "created_time": datetime.now(timezone.utc) - timedelta(days=5),
                "logged_exercises": [
                    ("Dips", 4, 10, 10),
                    ("Skullcrushers", 3, 12, 20),
                    ("Decline Cable Fly", 3, 12, 15)
                ],
                "workout_type": "Push"
            },
            {
                "notes": "Pull + Rotator Rehab",
                "created_time": datetime.now(timezone.utc) - timedelta(days=2),
                "logged_exercises": [
                    ("SA Lat Pulldown", 3, 10, 35),
                    ("Rotator Cuff", 3, 20, 2.5),
                    ("Incline DB Preachers", 3, 10, 12.5)
                ],
                "workout_type": "Pull"
            }
        ]
    }
]

def seed_users_and_workouts(db: Session):
    for user_data in sample_users:
        user = db.query(User).filter(User.username == user_data["username"]).first()
        if not user:
            user = User(username=user_data["username"], email=user_data["email"])
            db.add(user)
            db.commit()
            print(f"Created user: {user.username}")
        else:
            print(f"User '{user.username}' already exists.")

        for workout_data in user_data["workouts"]:
            existing_workout = db.query(Workout).filter(
                Workout.user_id == user.id,
                Workout.notes == workout_data["notes"],
                Workout.created_time == workout_data["created_time"]
            ).first()

            if existing_workout:
                print(f"Workout '{workout_data['notes']}' for {user.username} already exists.")
                continue

            workout = Workout(
                id=uuid.uuid4(),
                user_id=user.id,
                notes=workout_data["notes"],
                created_time=workout_data["created_time"],
                workout_type=WorkoutType(workout_data["workout_type"])
            )
            db.add(workout)
            db.flush()

            for name, sets, reps, weight in workout_data["logged_exercises"]:
                exercise = db.query(Exercise).filter(Exercise.name == name).first()
                if exercise:
                    log = LoggedExercise(
                        id=uuid.uuid4(),
                        workout_id=workout.id,
                        exercise_id=exercise.id,
                        sets=sets,
                        reps=reps,
                        weight=weight
                    )
                    db.add(log)
                else:
                    print(f"Warning: Exercise '{name}' not found.")

            print(f"Seeded workout for {user.username}: {workout.notes}")
    db.commit()

def populate_exercises(db: Session):
    seen = set()
    for category, exercises in exercise_data.items():
        for name, primary, secondary, description in exercises:
            if name in seen:
                continue
            seen.add(name)
            exists = db.query(Exercise).filter(Exercise.name == name).first()
            if not exists:
                ex = Exercise(
                    id=uuid.uuid4(),
                    name=name,
                    primary_muscles=primary,
                    secondary_muscles=secondary or None,
                    description=description
                )
                db.add(ex)
                print(f"Added exercise: {name}")
            else:
                print(f"Exercise '{name}' already exists.")
    db.commit()

def main():
    db = SessionLocal()
    try:
        populate_exercises(db)
        seed_users_and_workouts(db)
    finally:
        db.close()

if __name__ == "__main__":
    main()