import React, { useState, useEffect } from "react";
import axios from "axios";

const BASE_URL = "http://18.191.202.36:8000";

const createDefaultSet = (set_number = 1) => ({ set_number, reps: 8, weight: 0 });

const createDefaultExercise = (exerciseName = "") => ({
  exercise: { name: exerciseName },
  sets: [createDefaultSet()],
});

export default function UpdateWorkout() {
  const [workouts, setWorkouts] = useState([]);
  const [selectedWorkout, setSelectedWorkout] = useState(null);
  const [notes, setNotes] = useState("");
  const [workoutType, setWorkoutType] = useState("");
  const [message, setMessage] = useState("");
  const [username, setUsername] = useState("");
  const [categories, setCategories] = useState([]);
  const [groupedExercises, setGroupedExercises] = useState({});

  useEffect(() => {
    axios.get(`${BASE_URL}/exercises/categories`).then((res) => setCategories(res.data));
    axios.get(`${BASE_URL}/exercises/categorized`).then((res) => setGroupedExercises(res.data));
  }, []);

  const fetchWorkoutsByUser = async () => {
    try {
      const res = await axios.get(`${BASE_URL}/workouts/user/${username}`);
      setWorkouts(res.data);
    } catch (err) {
      console.error("Failed to fetch workouts", err);
    }
  };

  const handleSelectWorkout = (id) => {
    const workout = workouts.find((w) => w.id === id);
    if (!workout) return;
    setSelectedWorkout(JSON.parse(JSON.stringify(workout)));
    setNotes(workout.notes || "");
    setWorkoutType(workout.workout_type || "");
  };

  const updateExerciseName = (exIndex, name) => {
    const updated = { ...selectedWorkout };
    updated.logged_exercises[exIndex].exercise.name = name;
    setSelectedWorkout(updated);
  };

  const updateSetValue = (exIndex, setIndex, field, value) => {
    const updatedWorkout = { ...selectedWorkout };
    updatedWorkout.logged_exercises[exIndex].sets[setIndex][field] = value;
    setSelectedWorkout(updatedWorkout);
  };

  const addSet = (exIndex) => {
    const updated = { ...selectedWorkout };
    const sets = updated.logged_exercises[exIndex].sets;
    const nextSetNumber = sets.length + 1;
    sets.push(createDefaultSet(nextSetNumber));
    setSelectedWorkout(updated);
  };

  const removeSet = (exIndex, setIndex) => {
    const updated = { ...selectedWorkout };
    updated.logged_exercises[exIndex].sets = updated.logged_exercises[exIndex].sets.filter((_, i) => i !== setIndex);
    updated.logged_exercises[exIndex].sets.forEach((s, i) => s.set_number = i + 1);
    setSelectedWorkout(updated);
  };

  const addExercise = () => {
    const updated = { ...selectedWorkout };
    updated.logged_exercises.push(createDefaultExercise());
    setSelectedWorkout(updated);
  };

  const removeExercise = (exIndex) => {
    const updated = { ...selectedWorkout };
    updated.logged_exercises = updated.logged_exercises.filter((_, i) => i !== exIndex);
    setSelectedWorkout(updated);
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
      await axios.patch(`${BASE_URL}/workouts/${selectedWorkout.id}`, payload);
      setMessage("Workout updated successfully!");
      await fetchWorkoutsByUser();
    } catch (err) {
      console.error("Update failed", err);
      setMessage("Update failed: " + (err.response?.data?.detail || "Unknown error"));
    }
  };

  const handleDeleteWorkout = async () => {
    if (!selectedWorkout) return;

    try {
      await axios.delete(`${BASE_URL}/workouts/${selectedWorkout.id}`);
      setMessage("Workout deleted successfully.");
      setSelectedWorkout(null);
      setNotes("");
      setWorkoutType("");
      await fetchWorkoutsByUser();
    } catch (err) {
      console.error("Delete failed", err);
      setMessage("Failed to delete workout.");
    }
  };

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

          {selectedWorkout.logged_exercises.map((ex, exIndex) => (
            <div key={exIndex} className="border p-3 mb-4 rounded">
              <div className="d-flex justify-content-between align-items-center mb-2">
                <h6 className="mb-0">Exercise {exIndex + 1}</h6>
                <button
                  className="btn btn-sm btn-outline-danger"
                  onClick={() => removeExercise(exIndex)}
                >
                  Remove Exercise
                </button>
              </div>
              <select
                className="form-select mb-3"
                value={ex.exercise.name}
                onChange={(e) => updateExerciseName(exIndex, e.target.value)}
              >
                <option value="">Select an exercise</option>
                {Object.entries(groupedExercises).map(([category, exercises]) => (
                  <optgroup key={category} label={category}>
                    {exercises.map((exercise) => (
                      <option key={exercise.id} value={exercise.name}>
                        {exercise.name}
                      </option>
                    ))}
                  </optgroup>
                ))}
              </select>

              <div className="row fw-bold mb-2">
                <div className="col-2">Set #</div>
                <div className="col-5">Reps</div>
                <div className="col-5">Weight (lb)</div>
              </div>

              {ex.sets.map((set, setIndex) => (
                <div key={setIndex} className="row mb-2 align-items-center">
                  <div className="col-2">{set.set_number}</div>
                  <div className="col-5">
                    <input
                      type="number"
                      className="form-control"
                      value={set.reps}
                      onChange={(e) => updateSetValue(exIndex, setIndex, "reps", parseInt(e.target.value))}
                    />
                  </div>
                  <div className="col-5 d-flex">
                    <input
                      type="number"
                      className="form-control me-2"
                      value={set.weight}
                      onChange={(e) => updateSetValue(exIndex, setIndex, "weight", parseFloat(e.target.value))}
                    />
                    <button
                      className="btn btn-sm btn-outline-danger"
                      onClick={() => removeSet(exIndex, setIndex)}
                    >
                      ×
                    </button>
                  </div>
                </div>
              ))}

              <button
                className="btn btn-sm btn-outline-primary mt-2"
                onClick={() => addSet(exIndex)}
              >
                + Add Set
              </button>
            </div>
          ))}

          <button className="btn btn-outline-primary mb-3" onClick={addExercise}>
            + Add Exercise
          </button>

          <div className="d-flex gap-3">
            <button className="btn btn-primary" onClick={handleUpdate}>
              Submit Update
            </button>
            <button className="btn btn-danger" onClick={handleDeleteWorkout}>
              Delete Workout
            </button>
          </div>
        </>
      )}

      {message && <div className="alert alert-info mt-3">{message}</div>}
    </div>
  );
}