from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, insert
engine = create_engine('postgresql://localhost/fisitrackdb')
meta = MetaData()


### Create Users Table
user = Table(
   'user', meta,
   Column('user_id', Integer, primary_key = True),
   Column('name', String),
   Column('email', String),
)
meta.create_all(engine)

first_dummy_user = (
    insert(user).
    values(name='User1', email='abc@email.com')
)

with engine.connect() as conn:
    result = conn.execute(first_dummy_user)
    conn.commit()