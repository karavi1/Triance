import React, { useEffect, useState } from "react";
import axios from "axios";

const BASE_URL = "http://18.191.202.36:8000/exercises";

export default function Exercises() {
  const [exercises, setExercises] = useState([]);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [exerciseId, setExerciseId] = useState("");
  const [updatedName, setUpdatedName] = useState("");
  const [updateMessage, setUpdateMessage] = useState("");
  const [deleteMessage, setDeleteMessage] = useState("");

  const fetchAll = async () => {
    try {
      const res = await axios.get(BASE_URL + "/");
      setExercises(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const fetchById = async () => {
    try {
      const res = await axios.get(`${BASE_URL}/${exerciseId}`);
      setExercises([res.data]);
    } catch (err) {
      console.error("Error fetching by ID", err);
    }
  };

  const createExercise = async () => {
    try {
      await axios.post(BASE_URL + "/", { name, description });
      setName("");
      setDescription("");
      fetchAll();
    } catch (err) {
      console.error("Create failed", err);
    }
  };

  const updateExercise = async () => {
    try {
      await axios.patch(BASE_URL + "/", {
        exercise_id: exerciseId,
        updates: { name: updatedName },
      });
      setUpdateMessage("✅ Updated successfully!");
      fetchAll();
    } catch (err) {
      console.error("Update failed", err);
      setUpdateMessage("❌ Update failed.");
    }
  };

  const deleteExercise = async () => {
    try {
      await axios.delete(`${BASE_URL}/${exerciseId}`);
      setDeleteMessage("✅ Deleted successfully!");
      fetchAll();
    } catch (err) {
      console.error("Delete failed", err);
      setDeleteMessage("❌ Delete failed.");
    }
  };

  useEffect(() => {
    fetchAll();
  }, []);

  return (
    <div className="container mt-5 mb-5">
      <h2 className="mb-4">Exercise Manager</h2>

      {/* Create Exercise */}
      <div className="card p-4 mb-4">
        <h5 className="mb-3">Create New Exercise</h5>
        <div className="mb-3">
          <input
            className="form-control mb-2"
            placeholder="Exercise Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
          <input
            className="form-control"
            placeholder="Description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />
        </div>
        <button className="btn btn-primary" onClick={createExercise}>
          Create
        </button>
      </div>

      {/* Get by ID */}
      <div className="card p-4 mb-4">
        <h5 className="mb-3">Get Exercise by ID</h5>
        <div className="input-group">
          <input
            className="form-control"
            placeholder="Exercise ID"
            value={exerciseId}
            onChange={(e) => setExerciseId(e.target.value)}
          />
          <button className="btn btn-success" onClick={fetchById}>
            Fetch
          </button>
        </div>
      </div>

      {/* Update */}
      <div className="card p-4 mb-4">
        <h5 className="mb-3">Update Exercise</h5>
        <div className="mb-3">
          <input
            className="form-control"
            placeholder="Updated Name"
            value={updatedName}
            onChange={(e) => setUpdatedName(e.target.value)}
          />
        </div>
        <button className="btn btn-warning text-white" onClick={updateExercise}>
          Update
        </button>
        {updateMessage && (
          <div className="mt-2 alert alert-info">{updateMessage}</div>
        )}
      </div>

      {/* Delete */}
      <div className="card p-4 mb-4">
        <h5 className="mb-3">Delete Exercise</h5>
        <button className="btn btn-danger" onClick={deleteExercise}>
          Delete
        </button>
        {deleteMessage && (
          <div className="mt-2 alert alert-warning">{deleteMessage}</div>
        )}
      </div>

      {/* List Exercises */}
      <div className="card p-4">
        <h5 className="mb-3">All Exercises</h5>
        {exercises.length === 0 ? (
          <p className="text-muted">No exercises found.</p>
        ) : (
          <ul className="list-group">
            {exercises.map((ex) => (
              <li key={ex.id} className="list-group-item d-flex justify-content-between align-items-center">
                <div>
                  <strong>{ex.name}</strong>
                  <div className="text-muted small">
                    {ex.description || "No description"}
                  </div>
                </div>
                <span className="badge bg-secondary">{ex.id.slice(0, 6)}...</span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}