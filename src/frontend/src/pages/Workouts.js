import React, { useState } from "react";
import axios from "axios";
import CreateWorkout from "./CreateWorkout";

const BASE_URL = "http://18.191.202.36:8000";

export default function Workouts() {
  const [workoutId, setWorkoutId] = useState("");
  const [username, setUsername] = useState("");
  const [type, setType] = useState("Push");
  const [singleWorkout, setSingleWorkout] = useState(null);
  const [message, setMessage] = useState("");

  const fetchById = async () => {
    try {
      const res = await axios.get(`${BASE_URL}/workouts/workout_id/${workoutId}`);
      setSingleWorkout(res.data);
      setMessage("");
    } catch (err) {
      setSingleWorkout(null);
      setMessage("❌ Workout not found");
    }
  };

  const fetchByUser = async () => {
    try {
      const res = await axios.get(`${BASE_URL}/workouts/user/${username}`);
      const latest = res.data[res.data.length - 1];
      setSingleWorkout(latest);
      setMessage("");
    } catch (err) {
      setSingleWorkout(null);
      setMessage("⚠️ No workouts for that user");
    }
  };

  const fetchLatestByUser = async () => {
    try {
      const res = await axios.get(`${BASE_URL}/workouts/latest/user/${username}`);
      setSingleWorkout(res.data);
      setMessage("");
    } catch (err) {
      setSingleWorkout(null);
      setMessage("⚠️ No latest workout found");
    }
  };

  const fetchLatestByUserAndType = async () => {
    try {
      const res = await axios.get(`${BASE_URL}/workouts/${username}/latest/${type}`);
      setSingleWorkout(res.data);
      setMessage("");
    } catch (err) {
      setSingleWorkout(null);
      setMessage("⚠️ No workout of this type found for user");
    }
  };

  return (
    <div className="container mt-5 mb-5">
      <h2 className="mb-4">Workout Manager</h2>

      {message && <div className="alert alert-info">{message}</div>}

      {/* Workout Lookup by ID */}
      <div className="card p-3 mb-4">
        <h5>Get Workout by ID</h5>
        <div className="input-group">
          <input
            className="form-control"
            placeholder="Workout ID"
            value={workoutId}
            onChange={(e) => setWorkoutId(e.target.value)}
          />
          <button className="btn btn-primary" onClick={fetchById}>
            Fetch
          </button>
        </div>
      </div>

      {/* Workout Lookup by User */}
      <div className="card p-3 mb-4">
        <h5>Get Workout by Username</h5>
        <div className="input-group mb-2">
          <input
            className="form-control"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <button className="btn btn-outline-primary" onClick={fetchByUser}>
            Get All (Most Recent Shown)
          </button>
          <button className="btn btn-outline-secondary" onClick={fetchLatestByUser}>
            Get Latest Workout
          </button>
        </div>

        <div className="d-flex align-items-center gap-2">
          <select
            className="form-select"
            value={type}
            onChange={(e) => setType(e.target.value)}
          >
            <option value="Push">Push</option>
            <option value="Pull">Pull</option>
            <option value="Quads">Quads</option>
            <option value="Hams">Hams</option>
            <option value="Upper">Upper</option>
            <option value="Lower">Lower</option>
            <option value="Full Body">Full Body</option>
            <option value="Custom">Custom</option>
          </select>
          <button className="btn btn-outline-success" onClick={fetchLatestByUserAndType}>
            Get Latest by Type
          </button>
        </div>
      </div>

      {/* Single Workout Display */}
      {singleWorkout && (
        <div className="card p-3 mb-4">
          <h5>Workout Details</h5>
          <p><strong>User:</strong> {singleWorkout.username}</p>
          <p><strong>Workout Type:</strong> {singleWorkout.workout_type || "N/A"}</p>
          <p><strong>Date:</strong> {new Date(singleWorkout.created_time || singleWorkout.workout_date).toLocaleString()}</p>

          <ul className="list-group mt-3">
            {singleWorkout.logged_exercises.map((ex, idx) => (
              <li key={idx} className="list-group-item">
                <strong>{ex.exercise_name}</strong>
                <ul className="ms-3">
                  {ex.sets.map((s, j) => (
                    <li key={j}>
                      Set {s.set_number}: {s.reps} reps @ {s.weight}kg
                    </li>
                  ))}
                </ul>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Create Workout Form */}
      <div className="card p-3">
        <h5 className="mb-3">Create a New Workout</h5>
        <CreateWorkout />
      </div>
    </div>
  );
}