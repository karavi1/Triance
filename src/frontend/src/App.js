import React, { useState } from "react";
import axios from "axios";

function App() {
  const [message, setMessage] = useState("");
  const [users, setUsers] = useState([]);
  const [error, setError] = useState("");

  // Fetch the message from the root endpoint (for initial page load)
  useState(() => {
    setError(""); // Clear previous errors
    axios
      .get("http://18.119.104.96:8000/")
      .then((response) => {
        if (response && response.data && response.data.message) {
          setMessage(response.data.message);
        } else {
          setError("Unexpected response format from root endpoint.");
        }
      })
      .catch((err) => {
        if (err.response) {
          setError(
            `Backend error: ${err.response.status} - ${err.response.data.message || "Unknown error"}`
          );
        } else if (err.request) {
          setError("Network error: Unable to reach the backend.");
        } else {
          setError(`Error: ${err.message}`);
        }
      });
  }, []);

  // Function to fetch users when the button is clicked
  const fetchUsers = () => {
    setError(""); // Clear previous errors
    axios
      .get("http://18.119.104.96:8000/users")
      .then((response) => {
        if (response && response.data) {
          setUsers(response.data); // Assuming the response data is a list of users
        } else {
          setError("Unexpected response format from /users endpoint.");
        }
      })
      .catch((err) => {
        if (err.response) {
          setError(
            `Backend error: ${err.response.status} - ${err.response.data.message || "Unknown error"}`
          );
        } else if (err.request) {
          setError("Network error: Unable to reach the backend.");
        } else {
          setError(`Error: ${err.message}`);
        }
      });
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h1>Fitness Tracker</h1>
      {error ? (
        <div style={{ color: "red" }}>
          <strong>Error:</strong> {error}
        </div>
      ) : (
        <>
          <p>{message}</p>
          <button onClick={fetchUsers}>Get All Users</button>
          <h2>Users</h2>
          {users.length > 0 ? (
            <ul>
              {users.map((user) => (
                <li key={user.id}>{user.name} - {user.email}</li>
              ))}
            </ul>
          ) : (
            <p>No users found.</p>
          )}
        </>
      )}
    </div>
  );
}

export default App;
