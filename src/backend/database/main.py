from sqlalchemy import create_engine, text, insert

engine = create_engine('postgresql://localhost/fisitrackdb')

with engine.connect() as connection:
    connection.execute(text("CREATE TABLE user ( int, y int)"))
    connection.execute(text("INSERT INTO sqlalchemy_test (x, y) VALUES (:x, :y)"), [{"x": 1, "y": 1}, {"x": 2, "y": 4}])
    connection.commit()
    result = connection.execute(text("select * from public.sqlalchemy_test"))
    for row in result:
        print("record:", row)
