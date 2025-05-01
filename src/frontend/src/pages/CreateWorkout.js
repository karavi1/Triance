import React, { useEffect, useState } from "react";
import axios from "axios";

const BASE_URL = "http://18.191.202.36:8000";

const createDefaultSet = (set_number = 1) => ({
  set_number,
  reps: 8,
  weight: 0,
});
const createDefaultExercise = () => ({
  exercise_name: "",
  sets: [createDefaultSet()],
});

export default function CreateWorkout() {
  const [username, setUsername] = useState("");
  const [notes, setNotes] = useState("");
  const [category, setCategory] = useState("");
  const [loggedExercises, setLoggedExercises] = useState([createDefaultExercise()]);
  const [message, setMessage] = useState("");

  const [users, setUsers] = useState([]);
  const [groupedExercises, setGroupedExercises] = useState({});
  const [categories, setCategories] = useState([]);

  useEffect(() => {
    axios.get(`${BASE_URL}/users`)
      .then((res) => setUsers(res.data))
      .catch((err) => console.error("Error fetching users:", err));

    axios.get(`${BASE_URL}/exercises/categorized`)
      .then((res) => setGroupedExercises(res.data))
      .catch((err) => console.error("Error fetching exercises:", err));

    axios.get(`${BASE_URL}/exercises/categories`)
      .then((res) => {
        if (Array.isArray(res.data)) setCategories(res.data);
        else throw new Error("Invalid category format");
      })
      .catch((err) => {
        console.error("Error fetching categories:", err);
        setCategories([]);
      });
  }, []);

  const handleExerciseChange = (index, field, value) => {
    const updated = [...loggedExercises];
    updated[index][field] = value;
    setLoggedExercises(updated);
  };

  const handleSetChange = (exIndex, setIndex, field, value) => {
    const updated = [...loggedExercises];
    updated[exIndex].sets[setIndex][field] = value === "" ? "" : Number(value);
    setLoggedExercises(updated);
  };

  const addSet = (exIndex) => {
    const updated = [...loggedExercises];
    const nextSetNumber = updated[exIndex].sets.length + 1;
    updated[exIndex].sets.push(createDefaultSet(nextSetNumber));
    setLoggedExercises(updated);
  };

  const removeSet = (exIndex, setIndex) => {
    const updated = [...loggedExercises];
    updated[exIndex].sets = updated[exIndex].sets.filter((_, i) => i !== setIndex);
    updated[exIndex].sets.forEach((set, idx) => (set.set_number = idx + 1));
    setLoggedExercises(updated);
  };

  const addExercise = () => {
    setLoggedExercises([...loggedExercises, createDefaultExercise()]);
  };

  const removeExercise = (index) => {
    setLoggedExercises(loggedExercises.filter((_, i) => i !== index));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");

    const payload = {
      username,
      notes,
      category,
      logged_exercises: loggedExercises.map((ex) => ({
        name: ex.exercise_name,
        sets: ex.sets,
      })),
    };

    try {
      await axios.post(`${BASE_URL}/workouts/`, payload);
      setMessage("Workout created successfully!");
      setUsername("");
      setNotes("");
      setCategory("");
      setLoggedExercises([createDefaultExercise()]);
    } catch (err) {
      console.error(err);
      setMessage("Failed to create workout.");
    }
  };

  return (
    <div className="container mt-5 mb-5">
      <form onSubmit={handleSubmit}>
        {message && <div className="alert alert-info">{message}</div>}

        {/* User */}
        <div className="mb-3">
          <label className="form-label">User</label>
          <select
            className="form-select"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          >
            <option value="">Select a user</option>
            {users.map((user) => (
              <option key={user.id} value={user.username}>
                {user.username} ({user.email})
              </option>
            ))}
          </select>
        </div>

        {/* Notes */}
        <div className="mb-3">
          <label className="form-label">Notes</label>
          <textarea
            className="form-control"
            placeholder="Optional notes..."
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
          />
        </div>

        {/* Category */}
        <div className="mb-3">
          <label className="form-label">Workout Type</label>
          <select
            className="form-select"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            required
          >
            <option value="">Select a category</option>
            {categories.map((cat, i) => (
              <option key={i} value={cat}>{cat}</option>
            ))}
          </select>
        </div>

        {/* Exercises */}
        <div className="mb-4">
          <h5>Exercises</h5>
          {loggedExercises.map((ex, exIndex) => (
            <div key={exIndex} className="card p-3 mb-3">
              <div className="mb-3">
                <label className="form-label">Exercise</label>
                <select
                  className="form-select"
                  value={ex.exercise_name}
                  onChange={(e) => handleExerciseChange(exIndex, "exercise_name", e.target.value)}
                  required
                >
                  <option value="">Select an exercise</option>
                  {Object.entries(groupedExercises).map(([category, exerciseList]) => (
                    <optgroup key={category} label={category}>
                      {exerciseList.map((exercise) => (
                        <option key={exercise.id} value={exercise.name}>
                          {exercise.name}
                        </option>
                      ))}
                    </optgroup>
                  ))}
                </select>
              </div>

              {/* Set Table */}
              <div className="mb-2">
                <label className="form-label">Sets</label>
                <table className="table table-sm">
                  <thead>
                    <tr>
                      <th>Set</th>
                      <th>Reps</th>
                      <th>Weight (lb)</th>
                      <th>Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    {ex.sets.map((set, setIndex) => (
                      <tr key={setIndex}>
                        <td>{set.set_number}</td>
                        <td>
                          <input
                            type="number"
                            className="form-control"
                            value={set.reps}
                            onChange={(e) => handleSetChange(exIndex, setIndex, "reps", e.target.value)}
                          />
                        </td>
                        <td>
                          <input
                            type="number"
                            className="form-control"
                            value={set.weight}
                            onChange={(e) => handleSetChange(exIndex, setIndex, "weight", e.target.value)}
                          />
                        </td>
                        <td>
                          <button
                            type="button"
                            className="btn btn-sm btn-outline-danger"
                            onClick={() => removeSet(exIndex, setIndex)}
                          >
                            Remove
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>

                <div className="d-flex justify-content-between align-items-center">
                  <button
                    type="button"
                    className="btn btn-sm btn-outline-primary"
                    onClick={() => addSet(exIndex)}
                  >
                    + Add Set
                  </button>
                  <button
                    type="button"
                    className="btn btn-sm btn-outline-danger"
                    onClick={() => removeExercise(exIndex)}
                  >
                    Remove Exercise
                  </button>
                </div>
              </div>
            </div>
          ))}

          <button
            type="button"
            className="btn btn-outline-primary"
            onClick={addExercise}
          >
            + Add Exercise
          </button>
        </div>

        <button type="submit" className="btn btn-success">
          Submit Workout
        </button>
      </form>
    </div>
  );
}