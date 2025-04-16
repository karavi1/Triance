import React, { useEffect, useState } from "react";
import axios from "axios";

const BASE_URL = "http://18.191.202.36:8000";

const emptyExercise = {
  exercise_name: "",
  sets: 3,
  reps: 10,
  weight: 0,
};

export default function CreateWorkout() {
  const [username, setUsername] = useState("");
  const [notes, setNotes] = useState("");
  const [category, setCategory] = useState("Push");
  const [loggedExercises, setLoggedExercises] = useState([emptyExercise]);
  const [message, setMessage] = useState("");

  const [users, setUsers] = useState([]);
  const [exercises, setExercises] = useState([]);

  useEffect(() => {
    axios
      .get(`${BASE_URL}/users`)
      .then((res) => setUsers(res.data))
      .catch((err) => console.error("Error fetching users:", err));

    axios
      .get(`${BASE_URL}/exercises`)
      .then((res) => setExercises(res.data))
      .catch((err) => console.error("Error fetching exercises:", err));
  }, []);

  const handleExerciseChange = (index, field, value) => {
    const updated = [...loggedExercises];
    updated[index][field] = ["sets", "reps", "weight"].includes(field)
      ? Number(value)
      : value;
    setLoggedExercises(updated);
  };

  const addExercise = () => {
    setLoggedExercises([...loggedExercises, { ...emptyExercise }]);
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
      logged_exercises: loggedExercises,
    };

    try {
      await axios.post(`${BASE_URL}/workouts/`, payload);
      setMessage("✅ Workout created successfully!");
      setUsername("");
      setNotes("");
      setCategory("Push");
      setLoggedExercises([emptyExercise]);
    } catch (err) {
      console.error(err);
      setMessage("❌ Failed to create workout.");
    }
  };

  return (
    <div className="container mt-5 mb-5">
      <h2 className="mb-4">Create Workout</h2>

      {message && <div className="alert alert-info">{message}</div>}

      <form onSubmit={handleSubmit}>
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
          >
            <option value="Push">Push</option>
            <option value="Pull">Pull</option>
            <option value="Quads">Quads</option>
            <option value="Hams">Hams</option>
          </select>
        </div>

        {/* Exercise Section */}
        <div className="mb-4">
          <h5>Exercises</h5>
          {loggedExercises.map((ex, idx) => (
            <div key={idx} className="card p-3 mb-3">
              <div className="mb-3">
                <label className="form-label">Exercise</label>
                <select
                  className="form-select"
                  value={ex.exercise_name}
                  onChange={(e) =>
                    handleExerciseChange(idx, "exercise_name", e.target.value)
                  }
                  required
                >
                  <option value="">Select an exercise</option>
                  {exercises.map((exOpt) => (
                    <option key={exOpt.id} value={exOpt.name}>
                      {exOpt.name}
                    </option>
                  ))}
                </select>
              </div>

              <div className="row g-2">
                <div className="col">
                  <input
                    type="number"
                    className="form-control"
                    placeholder="Sets"
                    value={ex.sets}
                    onChange={(e) =>
                      handleExerciseChange(idx, "sets", e.target.value)
                    }
                  />
                </div>
                <div className="col">
                  <input
                    type="number"
                    className="form-control"
                    placeholder="Reps"
                    value={ex.reps}
                    onChange={(e) =>
                      handleExerciseChange(idx, "reps", e.target.value)
                    }
                  />
                </div>
                <div className="col">
                  <input
                    type="number"
                    className="form-control"
                    placeholder="Weight (kg)"
                    value={ex.weight}
                    onChange={(e) =>
                      handleExerciseChange(idx, "weight", e.target.value)
                    }
                  />
                </div>
              </div>

              <button
                type="button"
                className="btn btn-sm btn-outline-danger mt-2"
                onClick={() => removeExercise(idx)}
              >
                Remove Exercise
              </button>
            </div>
          ))}

          <button
            type="button"
            className="btn btn-outline-primary"
            onClick={addExercise}
          >
            + Add Another Exercise
          </button>
        </div>

        {/* Submit Button */}
        <button type="submit" className="btn btn-success">
          Submit Workout
        </button>
      </form>
    </div>
  );
}
