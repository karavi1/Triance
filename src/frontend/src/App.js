import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import React from "react";
import {
    BrowserRouter as Router,
    Routes,
    Route,
    Link
} from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext";
import PrivateRoute from "./components/PrivateRoute";
import Dashboard from './pages/Dashboard';
import Home from "./pages/Home";
import Exercises from "./pages/Exercises";
import Workouts from "./pages/Workouts";
import Login from "./pages/Login";
import Education from "./pages/Education";

function Navbar() {
    const { token, logout } = useAuth();

    return (
        <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
            <div className="container-fluid">
                <Link className="navbar-brand" to="/">Triance</Link>
                <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                    <span className="navbar-toggler-icon"></span>
                </button>

                <div className="collapse navbar-collapse" id="navbarNav">
                    <ul className="navbar-nav ms-auto">
                        {!token && (
                            <li className="nav-item">
                                <Link className="nav-link" to="/">Login</Link>
                            </li>
                        )}
                        <li className="nav-item">
                            <Link className="nav-link" to="/education">Education</Link>
                        </li>
                        {token && (
                            <>
                                <li className="nav-item">
                                    <Link className="nav-link" to="/exercises">Exercises</Link>
                                </li>
                                <li className="nav-item">
                                    <Link className="nav-link" to="/workouts">Workouts</Link>
                                </li>
                                <li className="nav-item">
                                    <Link className="nav-link" to="/dashboard">Dashboard</Link>
                                </li>
                                <li className="nav-item">
                                    <button
                                        className="btn btn-link nav-link"
                                        onClick={logout}
                                    >
                                        Logout
                                    </button>
                                </li>
                            </>
                        )}
                    </ul>
                </div>
            </div>
        </nav>
    );
}

function AppRoutes() {
    const { token } = useAuth();

    return (
        <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/education" element={<Education />} />

            <Route
                path="/exercises"
                element={<PrivateRoute><Exercises /></PrivateRoute>}
            />
            <Route
                path="/workouts"
                element={<PrivateRoute><Workouts /></PrivateRoute>}
            />
            <Route
                path="/dashboard"
                element={<PrivateRoute><Dashboard /></PrivateRoute>}
            />
        </Routes>
    );
}

export default function App() {
    return (
        <AuthProvider>
            <Router>
                <Navbar />
                <AppRoutes />
            </Router>
        </AuthProvider>
    );
}