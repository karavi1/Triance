import React, { useEffect, useState } from "react";
import axios from "axios";

if (!process.env.REACT_APP_BASE_URL) {
  throw new Error("REACT_APP_BASE_URL is not defined in the environment");
}

const BASE_URL = process.env.REACT_APP_BASE_URL;

export default function Users() {
  const [users, setUsers] = useState([]);
  const [selectedUser, setSelectedUser] = useState(null);
  const [message, setMessage] = useState("");

  // Create New User States
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");

  // Update Existing User States
  const [updatedEmail, setUpdatedEmail] = useState("");
  const [updatedUsername, setUpdatedUsername] = useState("");

  const createNewUser = async () => {
    try {
      const res = await axios.post(`${BASE_URL}/users/`, { email, username });
      setUsers((prev) => [...prev, res.data]); // Append new user to list
      setEmail("");
      setUsername("");
      setMessage("User created successfully");
    } catch (err) {
      setMessage("Failed to create new user");
      console.error(err);
    }
  };

  const updateExistingUser = async () => {
    if (!selectedUser) {
      setMessage("No user selected to update");
      return;
    }

    try {
      const res = await axios.patch(`${BASE_URL}/users/${selectedUser.id}`, {
        email: updatedEmail,
        username: updatedUsername,
      });
      setUsers((prev) =>
        prev.map((user) =>
          user.id === selectedUser.id ? res.data : user
        )
      );
      setUpdatedEmail("");
      setUpdatedUsername("");
      setMessage("User updated successfully");
    } catch (err) {
      setMessage("Failed to update user");
      console.error(err);
    }
  };

  const deleteUser = async (id) => {
    try {
      await axios.delete(`${BASE_URL}/users/${id}`);
      setUsers((prev) => prev.filter((user) => user.id !== id));
      setSelectedUser(null);
      setMessage("User deleted successfully");
    } catch (err) {
      setMessage("Failed to delete user");
      console.error(err);
    }
  };

  const fetchAllUsers = async () => {
    try {
      const res = await axios.get(`${BASE_URL}/users/`);
      if (process.env.NODE_ENV === "development") {
        console.log("Users response:", res.data);
      }
      setUsers(Array.isArray(res.data) ? res.data : []);
    } catch (err) {
      setMessage("Failed to fetch users");
      console.error(err);
      setUsers([]);
    }
  };

  useEffect(() => {
    fetchAllUsers();
  }, []);

  useEffect(() => {
    if (selectedUser) {
      setUpdatedUsername(selectedUser.username);
      setUpdatedEmail(selectedUser.email);
    } else {
      setUpdatedUsername("");
      setUpdatedEmail("");
    }
  }, [selectedUser]);

  return (
    <div className="container mt-5 mb-5">
      <h2 className="mb-4">User Manager</h2>

      {message && (
        <div className="alert alert-info alert-dismissible fade show" role="alert">
          {message}
          <button
            type="button"
            className="btn-close"
            aria-label="Close"
            onClick={() => setMessage("")}
          ></button>
        </div>
      )}

      {/* Create New User */}
      <div className="card p-3 mb-4">
        <h5>Create New User</h5>
        <div className="input-group">
          <input
            className="form-control"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <input
            className="form-control"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <button className="btn btn-primary" onClick={createNewUser}>
            Create
          </button>
        </div>
      </div>

      {/* Update Existing User */}
      <div className="card p-3 mb-4">
        <h5>Update Existing User</h5>

        <div className="mb-3">
          <select
            className="form-select"
            value={selectedUser?.id || ""}
            onChange={(e) => {
              const userId = e.target.value;
              const user = users.find((u) => u.id === userId);
              setSelectedUser(user || null);
            }}
          >
            <option value="">Select a user to update</option>
            {users.map((user) => (
              <option key={user.id} value={user.id}>
                {user.username} — {user.email}
              </option>
            ))}
          </select>
        </div>

        {selectedUser && (
          <>
            <div className="input-group mb-2">
              <input
                className="form-control"
                placeholder="Username"
                value={updatedUsername}
                onChange={(e) => setUpdatedUsername(e.target.value)}
              />
              <input
                className="form-control"
                placeholder="Email"
                value={updatedEmail}
                onChange={(e) => setUpdatedEmail(e.target.value)}
              />
            </div>
            <div className="d-flex gap-2">
              <button className="btn btn-primary" onClick={updateExistingUser}>
                Update
              </button>
              <button
                className="btn btn-danger"
                onClick={() => deleteUser(selectedUser.id)}
              >
                Delete
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}