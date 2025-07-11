import React from "react";
import { useAuth } from "../context/AuthContext";
import { Link } from "react-router-dom";
import Login from "./Login";

export default function Home() {
    const { user, token } = useAuth();

    if (!token) {
        return (
            <div className="container mt-5" style={{ maxWidth: 400 }}>
                <h2 className="mb-4 text-center">Welcome to Triance</h2>
                <Login />
            </div>
        );
    }

    return (
        <div className="container text-center mt-5">
            <h1 className="mb-4">Welcome to Triance, {user.username}!</h1>
            <p className="text-muted mb-5">
                Track your workouts, visualize your progress, and stay consistent.
            </p>
            <Link to="/exercises" className="btn btn-secondary me-2 mb-2">
                Manage Exercises
            </Link>
            <Link to="/workouts" className="btn btn-primary me-2 mb-2">
                Manage Workouts
            </Link>
            <Link to="/dashboard" className="btn btn-success mb-2">
                View Dashboard
            </Link>
        </div>
    );
}