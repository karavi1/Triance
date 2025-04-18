import React, { useState, useEffect } from "react";
import axios from "axios";

const BASE_URL = "http://18.191.202.36:8000/workouts";

export default function UpdateWorkout() {
  const [workouts, setWorkouts] = useState([]);
  const [selectedWorkout, setSelectedWorkout] = useState(null);
  const [notes, setNotes] = useState("");
  const [workoutType, setWorkoutType] = useState("");
  const [message, setMessage] = useState("");
  const [username, setUsername] = useState("");
  const [categories, setCategories] = useState([]);

  const fetchWorkoutsByUser = async () => {
    try {
      const res = await axios.get(`${BASE_URL}/user/${username}`);
      setWorkouts(res.data);
    } catch (err) {
      console.error("Failed to fetch workouts for user: " + username, err);
    }
  };

  const fetchCategories = async () => {
    try {
      const res = await axios.get("http://18.191.202.36:8000/exercises/categories");
      setCategories(res.data);
    } catch (err) {
      console.error("Failed to load categories", err);
    }
  };

  const handleSelectWorkout = (id) => {
    const workout = workouts.find((w) => w.id === id);
    if (!workout) return;
    setSelectedWorkout(workout);
    setNotes(workout.notes || "");
    setWorkoutType(workout.workout_type || "");
  };

  const handleUpdate = async () => {
    if (!selectedWorkout) return;

    const payload = {
      notes,
      workout_type: workoutType,
      logged_exercises: selectedWorkout.logged_exercises.map((le) => ({
        exercise_name: le.exercise.name,
        sets: le.sets.map((s) => ({
          set_number: s.set_number,
          reps: s.reps,
          weight: s.weight,
        })),
      })),
    };

    try {
      await axios.patch(`${BASE_URL}/${selectedWorkout.id}`, payload);
      setMessage("Workout updated successfully!");
      await fetchWorkoutsByUser();
    } catch (err) {
      console.error("Update failed", err);
      if (err.response?.data) {
        console.error("Backend error:", err.response.data);
        setMessage("Update failed: " + JSON.stringify(err.response.data));
      } else {
        setMessage("Update failed.");
      }
    }
  };

  const updateSetValue = (exIndex, setIndex, field, value) => {
    const updatedWorkout = { ...selectedWorkout };
    const updatedSet = {
      ...updatedWorkout.logged_exercises[exIndex].sets[setIndex],
    };

    updatedSet[field] = value;

    updatedWorkout.logged_exercises[exIndex].sets[setIndex] = updatedSet;
    setSelectedWorkout(updatedWorkout);
  };

  useEffect(() => {
    fetchCategories();
  }, []);

  return (
    <div className="card p-4">
      <div className="input-group mb-2">
        <input
          className="form-control"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <button className="btn btn-outline-primary" onClick={fetchWorkoutsByUser}>
          Fetch Workouts by user
        </button>
      </div>

      <div className="mb-3">
        <select
          className="form-select"
          value={selectedWorkout?.id || ""}
          onChange={(e) => handleSelectWorkout(e.target.value)}
        >
          <option value="">Select a workout to edit</option>
          {workouts.map((w) => (
            <option key={w.id} value={w.id}>
              {w.notes?.slice(0, 30) || "No notes"} — {w.workout_type}
            </option>
          ))}
        </select>
      </div>

      {selectedWorkout && (
        <>
          <div className="mb-3">
            <label>Notes</label>
            <textarea
              className="form-control"
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
            />
          </div>

          <div className="mb-3">
            <label>Workout Type</label>
            <select
              className="form-select"
              value={workoutType}
              onChange={(e) => setWorkoutType(e.target.value)}
            >
              <option value="">Select workout type</option>
              {categories.map((type) => (
                <option key={type} value={type}>
                  {type}
                </option>
              ))}
            </select>
          </div>

          {selectedWorkout.logged_exercises.map((ex, exIndex) => {
            const sortedSets = [...ex.sets].sort(
              (a, b) => a.set_number - b.set_number
            );

            return (
              <div key={exIndex} className="border p-3 mb-4 rounded">
                <h6 className="mb-3">{ex.exercise.name}</h6>

                <div className="row fw-bold mb-2">
                  <div className="col-2">Set #</div>
                  <div className="col-5">Reps</div>
                  <div className="col-5">Weight (lb)</div>
                </div>

                {sortedSets.map((set, setIndex) => (
                  <div key={setIndex} className="row mb-2 align-items-center">
                    <div className="col-2">
                      <span>{set.set_number}</span>
                    </div>
                    <div className="col-5">
                      <input
                        type="number"
                        className="form-control"
                        value={set.reps}
                        onChange={(e) =>
                          updateSetValue(
                            exIndex,
                            set.set_number - 1,
                            "reps",
                            parseInt(e.target.value)
                          )
                        }
                      />
                    </div>
                    <div className="col-5">
                      <input
                        type="number"
                        className="form-control"
                        value={set.weight}
                        onChange={(e) =>
                          updateSetValue(
                            exIndex,
                            set.set_number - 1,
                            "weight",
                            parseFloat(e.target.value)
                          )
                        }
                      />
                    </div>
                  </div>
                ))}
              </div>
            );
          })}

          <button className="btn btn-primary mt-2" onClick={handleUpdate}>
            Submit Update
          </button>
        </>
      )}

      {message && <div className="alert alert-info mt-3">{message}</div>}
    </div>
  );
}