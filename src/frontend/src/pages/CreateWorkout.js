import React, { useEffect, useState } from "react";
import axios from "axios";
import Toast from "react-bootstrap/Toast";
import ToastContainer from "react-bootstrap/ToastContainer";

if (!process.env.REACT_APP_BASE_URL) {
  throw new Error("REACT_APP_BASE_URL is not defined in the environment");
}

const BASE_URL = process.env.REACT_APP_BASE_URL;

const createDefaultSet = (set_number = 1) => ({
  set_number,
  reps: 8,
  weight: 0,
});

const createDefaultExercise = () => ({
  exercise_name: "",
  sets: [createDefaultSet()],
});

function formatToDatetimeLocal(isoString) {
  const date = new Date(isoString);
  const tzOffset = date.getTimezoneOffset() * 60000;
  return new Date(date.getTime() - tzOffset).toISOString().slice(0, 16);
}

export default function CreateWorkout() {
  const [username, setUsername] = useState("");
  const [notes, setNotes] = useState("");
  const [category, setCategory] = useState("");
  const [loggedExercises, setLoggedExercises] = useState([createDefaultExercise()]);
  const [users, setUsers] = useState([]);
  const [groupedExercises, setGroupedExercises] = useState({});
  const [categories, setCategories] = useState([]);
  const [toast, setToast] = useState({ show: false, message: "", variant: "info" });
  const [createdTime, setCreatedTime] = useState(() => {
    const now = new Date();
    return new Date(now.getTime() - now.getTimezoneOffset() * 60000)
      .toISOString()
      .slice(0, 16);
  });

  useEffect(() => {
    axios.get(`${BASE_URL}/users`)
      .then((res) => setUsers(res.data))
      .catch((err) => console.error("Error fetching users:", err));

    axios.get(`${BASE_URL}/exercises/categorized`)
      .then((res) => {
        if (res.data && typeof res.data === "object") setGroupedExercises(res.data);
        else throw new Error("Invalid exercise format");
      })
      .catch((err) => {
        console.error("Error fetching exercises:", err);
        setGroupedExercises({});
      });

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

  const showToast = (message, variant = "info") => {
    setToast({ show: true, message, variant });
    setTimeout(() => setToast({ show: false, message: "", variant: "info" }), 4000);
  };

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

    const payload = {
      username,
      created_time: createdTime ? formatToDatetimeLocal(createdTime) : undefined,
      notes,
      workout_type: category,
      logged_exercises: loggedExercises.map((ex) => ({
        name: ex.exercise_name,
        sets: ex.sets,
      })),
    };

    try {
      await axios.post(`${BASE_URL}/workouts/`, payload);
      showToast("Workout created successfully!", "success");
      setUsername("");
      setNotes("");
      setCategory("");
      setLoggedExercises([createDefaultExercise()]);
    } catch (err) {
      console.error(err);
      showToast("Failed to create workout.", "danger");
    }
  };

  return (
    <div className="container mt-5 mb-5 position-relative">
      <ToastContainer className="position-absolute top-50 start-50 translate-middle" style={{ zIndex: 1060 }}>
        <Toast bg={toast.variant} show={toast.show} onClose={() => setToast({ ...toast, show: false })} delay={4000} autohide>
          <Toast.Body className="text-white text-center">{toast.message}</Toast.Body>
        </Toast>
      </ToastContainer>

      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label className="form-label">User</label>
          <select
            className="form-select"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          >
            <option value="">Select a user</option>
            {Array.isArray(users) && users.map((user) => (
              <option key={user.id} value={user.username}>
                {user.username} ({user.email})
              </option>
            ))}
          </select>
        </div>

        <div className="mb-3">
          <label className="form-label">Workout Type</label>
          <select
            className="form-select"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            required
          >
            <option value="">Select a category</option>
            {Array.isArray(categories) && categories.map((cat, i) => (
              <option key={i} value={cat}>{cat}</option>
            ))}
          </select>
        </div>

        <div className="mb-3">
          <label className="form-label">Workout Date & Time</label>
          <input
            type="datetime-local"
            className="form-control mb-3"
            value={createdTime}
            onChange={(e) => setCreatedTime(e.target.value)}
          />
        </div>

        <div className="mb-3">
          <label className="form-label">Notes</label>
          <textarea
            className="form-control"
            placeholder="Optional notes..."
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
          />
        </div>

        <div className="mb-4">
          <h5>Exercises</h5>
          {Array.isArray(loggedExercises) && loggedExercises.map((ex, exIndex) => (
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
                  {groupedExercises && typeof groupedExercises === "object" &&
                    Object.entries(groupedExercises).map(([category, exerciseList]) => (
                      <optgroup key={category} label={category}>
                        {Array.isArray(exerciseList) &&
                          exerciseList.map((exercise) => (
                            <option key={exercise.id} value={exercise.name}>
                              {exercise.name}
                            </option>
                          ))}
                      </optgroup>
                    ))}
                </select>
              </div>

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
                    {Array.isArray(ex.sets) && ex.sets.map((set, setIndex) => (
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