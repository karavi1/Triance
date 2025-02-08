from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, insert, ForeignKey

# TODO: change this to access aws aurora
engine = create_engine('postgresql://localhost/cft')
meta = MetaData()



### Create Users Table
users = Table(
   'users', meta,
   Column('user_id', Integer, primary_key = True),
   Column('name', String),
   Column('email', String),
)

### Create Exercise Table
exercises = Table(
    'exercises', meta,
    Column('exercise_id', Integer, primary_key = True),
    Column('name', String),
    Column('body_part', String),
    Column('sets', Integer),
    Column('reps', Integer),
    Column('weight', Integer),
)

### Create Workout Table
workouts = Table(
   'workouts', meta,
   Column('workout_id', Integer, primary_key = True),
   Column('user_id', ForeignKey("users.user_id")),
   Column('exercises', String), ## Temporarily serialize list to string here, use pickle: https://docs.python.org/3/library/pickle.html
)

meta.create_all(engine)

first_dummy_user = (
    insert(users).
    values(name='User1', email='abc@email.com')
)



with engine.connect() as conn:
    result = conn.execute(first_dummy_user)
    conn.commit()