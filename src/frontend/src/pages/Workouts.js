import React, { useState } from "react";
import axios from "axios";
import CreateWorkout from "./CreateWorkout";
import UpdateWorkout from "./UpdateWorkout";

if (!process.env.REACT_APP_BASE_URL) {
  throw new Error("REACT_APP_BASE_URL is not defined in the environment");
}

const BASE_URL = process.env.REACT_APP_BASE_URL;

export default function Workouts() {
  const [username, setUsername] = useState("");
  const [type, setType] = useState("Push");
  const [singleWorkout, setSingleWorkout] = useState(null);
  const [allWorkouts, setAllWorkouts] = useState([]);
  const [message, setMessage] = useState("");

  const fetchAllByUser = async () => {
    try {
      const res = await axios.get(`${BASE_URL}/workouts/user/${username}`);
      console.log("All workouts response:", res.data);
      const data = res.data;
      setAllWorkouts(Array.isArray(data) ? data : []);
      setSingleWorkout(null);
      setMessage(!Array.isArray(data) || data.length === 0 ? "No workouts found for user" : "");
    } catch (err) {
      console.error("Failed to fetch all workouts", err);
      setAllWorkouts([]);
      setMessage("No workouts for that user");
    }
  };

  const fetchLatestByUser = async () => {
    try {
      const res = await axios.get(`${BASE_URL}/workouts/user/${username}/latest`);
      console.log("Latest workout:", res.data);
      setSingleWorkout(res.data || null);
      setAllWorkouts([]);
      setMessage(!res.data ? "No latest workout found" : "");
    } catch (err) {
      console.error("Failed to fetch latest workout", err);
      setSingleWorkout(null);
      setMessage("No latest workout found");
    }
  };

  const fetchLatestByUserAndType = async () => {
    try {
      const res = await axios.get(`${BASE_URL}/workouts/user/${username}/latest/${type}`);
      console.log("Latest workout by type:", res.data);
      setSingleWorkout(res.data || null);
      setAllWorkouts([]);
      setMessage(!res.data ? "No workout of this type found for user" : "");
    } catch (err) {
      console.error("Failed to fetch latest workout by type", err);
      setSingleWorkout(null);
      setMessage("No workout of this type found for user");
    }
  };

  return (
    <div className="container mt-5 mb-5">
      <h2 className="mb-4">Workout Manager</h2>

      {message && <div className="alert alert-info">{message}</div>}

      {/* Lookup Controls */}
      <div className="card p-3 mb-4">
        <h5>Get Workout by Username</h5>
        <div className="input-group mb-2">
          <input
            className="form-control"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <button className="btn btn-outline-primary" onClick={fetchAllByUser}>
            Get All
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

      {/* Multiple Workouts */}
      {Array.isArray(allWorkouts) &&
        allWorkouts.map((workout, index) => (
          workout ? (
            <div key={index} className="card p-3 mb-4">
              <p><strong>Number:</strong> {index + 1}</p>
              <p><strong>ID:</strong> {workout.id}</p>
              <p><strong>Category:</strong> {workout.workout_type || "N/A"}</p>
              <p><strong>Date:</strong> {new Date(workout.created_time || workout.workout_date || Date.now()).toLocaleString()}</p>
            </div>
          ) : null
        ))}

      {/* Single Workout */}
      {singleWorkout && (
        <div className="card p-3 mb-4">
          <h5>Workout Details</h5>
          <p><strong>User:</strong> {username}</p>
          <p><strong>ID:</strong> {singleWorkout.id}</p>
          <p><strong>Category:</strong> {singleWorkout.workout_type || "N/A"}</p>
          <p><strong>Date:</strong> {new Date(singleWorkout.created_time || singleWorkout.workout_date || Date.now()).toLocaleString()}</p>

          <div className="table-responsive mt-3">
            {Array.isArray(singleWorkout.logged_exercises) &&
              singleWorkout.logged_exercises.map((logged_exercise, idx) => {
                const sortedSets = Array.isArray(logged_exercise.sets)
                  ? [...logged_exercise.sets].sort((a, b) => a.set_number - b.set_number)
                  : [];
                return (
                  <div key={idx} className="mb-4">
                    <h6>
                      <strong>
                        {logged_exercise.exercise_name ||
                          logged_exercise.exercise?.name ||
                          "Unnamed Exercise"}
                      </strong>
                    </h6>
                    <table className="table table-sm table-bordered">
                      <thead>
                        <tr>
                          <th>Set #</th>
                          <th>Reps</th>
                          <th>Weight (lb)</th>
                        </tr>
                      </thead>
                      <tbody>
                        {sortedSets.map((set, j) => (
                          <tr key={j}>
                            <td>{set.set_number}</td>
                            <td>{set.reps}</td>
                            <td>{set.weight}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                );
              })}
          </div>
        </div>
      )}

      {/* Create & Update Workout Collapsibles */}
      <div className="card p-3 mb-3">
        <button
          className="btn btn-link text-start fw-bold"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#createWorkoutCollapse"
          aria-expanded="false"
          aria-controls="createWorkoutCollapse"
        >
          Create a New Workout
        </button>
        <div className="collapse" id="createWorkoutCollapse">
          <CreateWorkout />
        </div>
      </div>

      <div className="card p-3 mb-3">
        <button
          className="btn btn-link text-start fw-bold"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#updateWorkoutCollapse"
          aria-expanded="false"
          aria-controls="updateWorkoutCollapse"
        >
          Update an Existing Workout
        </button>
        <div className="collapse" id="updateWorkoutCollapse">
          <UpdateWorkout />
        </div>
      </div>
    </div>
  );
}