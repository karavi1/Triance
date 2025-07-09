import pytest
from uuid import uuid4

from src.backend.crud import exercise as crud_exercise
from src.backend.schemas.exercise import ExerciseCreate, ExerciseUpdate
from src.backend.models.enums import ExerciseGroup


def test_create_exercise(db):
    exercise = ExerciseCreate(
        name="Deadlift",
        primary_muscles=["back", "glutes"],
        secondary_muscles=["hamstrings"],
        description="Posterior chain compound lift",
        category=ExerciseGroup.PULL
    )
    created = crud_exercise.create_exercise(db, exercise, None)

    assert created.id is not None
    assert created.name == "Deadlift"
    assert "glutes" in created.primary_muscles


def test_create_exercise_with_auth_user(db, test_user):
    exercise = ExerciseCreate(
        name="Bench Press",
        primary_muscles=["chest", "triceps"],
        secondary_muscles=["shoulders"],
        description="Upper-body push movement",
        category=ExerciseGroup.PUSH
    )
    created = crud_exercise.create_exercise(db, exercise, test_user)

    assert created.id is not None
    assert created.name == "Bench Press"
    assert created.user_id == test_user.id


def test_create_batch_exercise(db):
    e1 = ExerciseCreate(
        name="Deadlift",
        primary_muscles=["back", "glutes"],
        secondary_muscles=["hamstrings"],
        description="Posterior chain compound lift",
        category=ExerciseGroup.PULL
    )
    e2 = ExerciseCreate(
        name="Squat",
        primary_muscles=["quads", "glutes"],
        secondary_muscles=["hamstrings"],
        description="Leg compound lift",
        category=ExerciseGroup.QUADS
    )
    created = crud_exercise.create_batch_exercise(db, [e1, e2], None)
    assert len(created) == 2
    assert created[0].name == "Deadlift"
    assert created[1].primary_muscles[0] == "quads"


def test_create_batch_exercise_with_auth_user(db, test_user):
    e1 = ExerciseCreate(
        name=f"Test1_{uuid4().hex[:6]}",
        primary_muscles=["m1"],
        category=ExerciseGroup.PULL
    )
    e2 = ExerciseCreate(
        name=f"Test2_{uuid4().hex[:6]}",
        primary_muscles=["m2"],
        category=ExerciseGroup.PUSH
    )
    created = crud_exercise.create_batch_exercise(db, [e1, e2], test_user)
    assert all(ex.user_id == test_user.id for ex in created)


def test_get_exercise_by_id(db, test_user):
    created = crud_exercise.create_exercise(
        db,
        ExerciseCreate(
            name="Pull-up",
            primary_muscles=["lats", "biceps"],
            secondary_muscles=["shoulders"],
            description="Bodyweight upper-body pulling movement",
            category=ExerciseGroup.PULL
        ),
        None
    )
    fetched = crud_exercise.get_exercise_by_id(db, created.id, None)

    assert fetched.id == created.id
    assert fetched.name == "Pull-up"


def test_get_exercise_by_id_unauthorized(db, test_user, create_user):
    other = create_user(username="other", email="other@example.com", password="pass")
    exercise = crud_exercise.create_exercise(
        db,
        ExerciseCreate(
            name="Dip",
            primary_muscles=["triceps"],
            category=ExerciseGroup.PUSH
        ),
        other
    )
    fetched = crud_exercise.get_exercise_by_id(db, exercise.id, test_user)
    assert fetched is None


def test_get_all_exercises(db):
    crud_exercise.create_exercise(db, ExerciseCreate(
        name="Bench Press",
        primary_muscles=["chest", "triceps"],
        secondary_muscles=["shoulders"],
        category=ExerciseGroup.PUSH
    ), None)
    crud_exercise.create_exercise(db, ExerciseCreate(
        name="Squat",
        primary_muscles=["quads", "glutes"],
        category=ExerciseGroup.QUADS
    ), None)

    # pass None positionally; do not use user=None
    all_ex = crud_exercise.get_all_exercises(db, None)
    names = [ex.name for ex in all_ex]
    assert set(names) == {"Bench Press", "Squat"}


def test_get_all_exercises_authorization(db, test_user, create_user):
    crud_exercise.create_exercise(db, ExerciseCreate(name="Pub", primary_muscles=["a"], category=ExerciseGroup.PULL), None)
    owned = crud_exercise.create_exercise(db, ExerciseCreate(name="Own", primary_muscles=["b"], category=ExerciseGroup.PULL), test_user)
    other = create_user(username="other2", email="o2@example.com", password="pw")
    crud_exercise.create_exercise(db, ExerciseCreate(name="Other", primary_muscles=["c"], category=ExerciseGroup.PULL), other)

    results = crud_exercise.get_all_exercises(db, test_user)
    ids = [ex.id for ex in results]
    assert owned.id in ids
    assert all(ex.user_id != other.id for ex in results)


def test_get_all_exercises_categorized(db):
    p = crud_exercise.create_exercise(db, ExerciseCreate(name="A1", primary_muscles=["x"], category=ExerciseGroup.PULL), None)
    u = crud_exercise.create_exercise(db, ExerciseCreate(name="P1", primary_muscles=["y"], category=ExerciseGroup.PUSH), None)

    # pass None positionally
    grouped = crud_exercise.get_all_exercises_categorized(db, None)

    assert ExerciseGroup.PULL.value in grouped
    assert ExerciseGroup.PUSH.value in grouped
    assert any(ex.id == p.id for ex in grouped[ExerciseGroup.PULL.value])
    assert any(ex.id == u.id for ex in grouped[ExerciseGroup.PUSH.value])


def test_update_exercise(db, test_user):
    created = crud_exercise.create_exercise(
        db,
        ExerciseCreate(name="Row", primary_muscles=["back"], category=ExerciseGroup.PULL),
        test_user
    )
    updated = crud_exercise.update_exercise(
        db,
        created.id,
        ExerciseUpdate(name="Barbell Row", primary_muscles=["back", "biceps"]),
        test_user
    )
    assert updated is not None
    assert updated.name == "Barbell Row"
    assert "biceps" in updated.primary_muscles


def test_update_exercise_invalid_id(db, test_user):
    result = crud_exercise.update_exercise(db, uuid4(), ExerciseUpdate(name="X"), test_user)
    assert result is None


def test_update_exercise_unauthorized(db, test_user, create_user):
    other = create_user(username="other3", email="o3@example.com", password="pw")
    ex = crud_exercise.create_exercise(db, ExerciseCreate(name="Z", primary_muscles=["z"], category=ExerciseGroup.PULL), other)
    updated = crud_exercise.update_exercise(db, ex.id, ExerciseUpdate(name="NewZ"), test_user)
    assert updated is None


def test_delete_exercise(db, test_user):
    created = crud_exercise.create_exercise(db, ExerciseCreate(name="Press", primary_muscles=["s"], category=ExerciseGroup.PUSH), test_user)
    res = crud_exercise.delete_exercise(db, created.id, test_user)
    assert res is True
    assert crud_exercise.get_exercise_by_id(db, created.id, test_user) is None


def test_delete_exercise_invalid_id(db, test_user):
    assert not crud_exercise.delete_exercise(db, uuid4(), test_user)


def test_delete_exercise_unauthorized(db, test_user, create_user):
    other = create_user(username="other4", email="o4@example.com", password="pw")
    ex = crud_exercise.create_exercise(db, ExerciseCreate(name="Del", primary_muscles=["d"], category=ExerciseGroup.PULL), other)
    res = crud_exercise.delete_exercise(db, ex.id, test_user)
    assert res is False
    assert crud_exercise.get_exercise_by_id(db, ex.id, other) is not None


# Admin access behavior

def test_admin_can_update_any_exercise(db, create_user):
    owner = create_user("someone", "s@x.com", "pw")
    admin = create_user("admin1", "admin@a.com", "pw", is_admin=True)
    ex = crud_exercise.create_exercise(db, ExerciseCreate(name="AdminUpdate", primary_muscles=["x"], category=ExerciseGroup.PULL), owner)

    updated = crud_exercise.update_exercise(db, ex.id, ExerciseUpdate(name="AdminDidThis"), admin)
    assert updated is not None
    assert updated.name == "AdminDidThis"


def test_admin_can_delete_any_exercise(db, create_user):
    owner = create_user("someone2", "s2@x.com", "pw")
    admin = create_user("admin2", "admin2@a.com", "pw", is_admin=True)
    ex = crud_exercise.create_exercise(db, ExerciseCreate(name="AdminDel", primary_muscles=["x"], category=ExerciseGroup.PUSH), owner)

    deleted = crud_exercise.delete_exercise(db, ex.id, admin)
    assert deleted is True


def test_admin_sees_all_exercises(db, create_user):
    user1 = create_user("bob", "bob@x.com", "pw")
    user2 = create_user("jess", "jess@x.com", "pw")
    admin = create_user("admin3", "admin3@x.com", "pw", is_admin=True)

    crud_exercise.create_exercise(db, ExerciseCreate(name="Pub1", primary_muscles=["a"], category=ExerciseGroup.PULL), None)
    crud_exercise.create_exercise(db, ExerciseCreate(name="U1", primary_muscles=["b"], category=ExerciseGroup.PULL), user1)
    crud_exercise.create_exercise(db, ExerciseCreate(name="U2", primary_muscles=["c"], category=ExerciseGroup.PULL), user2)

    all_ex = crud_exercise.get_all_exercises(db, admin)
    names = [ex.name for ex in all_ex]
    assert {"Pub1", "U1", "U2"}.issubset(set(names))