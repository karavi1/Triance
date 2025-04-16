import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Home from "./pages/Home";
import Workouts from "./pages/Workouts";
import Exercises from "./pages/Exercises";
import Users from "./pages/Users"; // 👈 Import the Users page

function App() {
  return (
    <Router>
      {/* Bootstrap Navbar */}
      <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
        <div className="container-fluid">
          <Link className="navbar-brand" to="/">CFT</Link>
          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarNav"
          >
            <span className="navbar-toggler-icon"></span>
          </button>

          <div className="collapse navbar-collapse" id="navbarNav">
            <ul className="navbar-nav ms-auto">
              <li className="nav-item">
                <Link className="nav-link" to="/">Home</Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="/workouts">Workouts</Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="/exercises">Exercises</Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="/users">Users</Link> {/* ✅ Added Users link */}
              </li>
            </ul>
          </div>
        </div>
      </nav>

      {/* Page Routes */}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/workouts" element={<Workouts />} />
        <Route path="/exercises" element={<Exercises />} />
        <Route path="/users" element={<Users />} /> {/* ✅ Added Users route */}
      </Routes>
    </Router>
  );
}

export default App;