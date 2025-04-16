import React, { useState, useEffect } from "react";
import axios from "axios";

const BASE_URL = "http://18.191.202.36:8000";

function Home() {
  const [message, setMessage] = useState("");
  const [users, setUsers] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    axios
      .get(`${BASE_URL}/`)
      .then((res) => {
        setMessage(res.data?.message || "No message returned");
      })
      .catch((err) => {
        setError("Error fetching message: " + err.message);
      });
  }, []);

  return (
    <div className="container text-center mt-5">
      <h1 className="mb-4">🏋️‍♂️ Welcome to a Customizable Fitness Tracker!</h1>

      {error && <div className="alert alert-danger">{error}</div>}
      {message && <div className="alert alert-primary">{message}</div>}

      <p className="text-muted">Track your workouts, visualize your progress, and stay consistent.</p>

      <div className="mt-4">
        <a href="/workouts" className="btn btn-success me-2">
          View Workouts
        </a>
        <a href="/workouts/create" className="btn btn-outline-primary me-2">
          Log a Workout
        </a>
        <a href="/exercises" className="btn btn-secondary">
          Manage Exercises
        </a>
      </div>
    </div>
  );
}

export default Home;