import React, { useEffect, useState } from "react";
import axios from "axios";

const BASE_URL = "http://18.191.202.36:8000/users";

export default function Users() {
  const [users, setUsers] = useState([]);
  const [userId, setUserId] = useState("");
  const [selectedUser, setSelectedUser] = useState(null);
  const [message, setMessage] = useState("");

  const fetchAllUsers = async () => {
    try {
      const res = await axios.get(BASE_URL);
      setUsers(res.data);
      setMessage("");
    } catch (err) {
      setMessage("Failed to fetch users");
    }
  };

  const fetchUserById = async () => {
    if (!userId) return;

    try {
      const res = await axios.get(`${BASE_URL}/${userId}`);
      setSelectedUser(res.data);
      setMessage("");
    } catch (err) {
      setSelectedUser(null);
      setMessage("User not found");
    }
  };

  const deleteUser = async (id) => {
    try {
      await axios.delete(`${BASE_URL}/${id}`);
      setMessage("User deleted successfully");
      setSelectedUser(null);
      fetchAllUsers();
    } catch (err) {
      setMessage("Failed to delete user");
    }
  };

  useEffect(() => {
    fetchAllUsers();
  }, []);

  return (
    <div className="container mt-5 mb-5">
      <h2 className="mb-4">User Manager</h2>

      {message && <div className="alert alert-info">{message}</div>}

      {/* Search by ID */}
      <div className="card p-3 mb-4">
        <h5>Get User by ID</h5>
        <div className="input-group">
          <input
            className="form-control"
            placeholder="User ID"
            value={userId}
            onChange={(e) => setUserId(e.target.value)}
          />
          <button className="btn btn-primary" onClick={fetchUserById}>
            Fetch
          </button>
        </div>

        {selectedUser && (
          <div className="mt-3 border p-3 rounded bg-light">
            <p><strong>Username:</strong> {selectedUser.username}</p>
            <p><strong>Email:</strong> {selectedUser.email}</p>
            <p><strong>ID:</strong> {selectedUser.id}</p>
            <button
              className="btn btn-sm btn-danger"
              onClick={() => deleteUser(selectedUser.id)}
            >
              Delete This User
            </button>
          </div>
        )}
      </div>

      {/* All Users List */}
      <div className="card p-3">
        <h5>All Users</h5>
        {users.length === 0 ? (
          <p className="text-muted">No users found.</p>
        ) : (
          <ul className="list-group">
            {users.map((user) => (
              <li
                key={user.id}
                className="list-group-item d-flex justify-content-between align-items-center"
              >
                <div>
                  <strong>{user.username}</strong> — {user.email}
                  <div className="text-muted small">{user.id}</div>
                </div>
                <button
                  className="btn btn-sm btn-danger"
                  onClick={() => deleteUser(user.id)}
                >
                  Delete
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}