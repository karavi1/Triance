from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# class Item(BaseModel):
#     name: str
#     price: float
#     is_offer: Union[bool, None] = None

# @app.put("/items/{item_id}")
# def update_item(item_id: int, item: Item):
#     return {"item_name": item.name, "item_id": item_id}

@app.get("/cft/latest_workout/{user_id}")
def get_latest_workout(user_id: int):
    return {"workout": "sample workout" }

@app.get("/cft/all_workouts/{user_id}")
def get_all_workouts(user_id: int):
    return {"workout": "sample workout" }

@app.get("/cft/workout/{user_id})")
def get_specific_workout(user_id: int, workout_id: int):
    return {"workout": "sample workout" }

@app.put("/cft/{user_id}")
def create_user():
    print("something happens")

@app.put("/cft/{exercise_id}")
def create_exercise():
    return 2

@app.put("/cft/{workout_id}")
def create_workout():
    return 3

