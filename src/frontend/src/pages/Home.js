import React from "react";
import { useAuth } from "../context/AuthContext";
import { Link } from "react-router-dom";

export default function Home() {
    const { user, token } = useAuth();

    if (!token) {
        return (
            <div className="container text-center mt-5">
                <h1 className="mb-4">Welcome to Triance</h1>
                <p className="mb-4 text-muted">
                    Track your workouts, visualize your progress, and stay consistent.
                </p>
                <Link to="/signup" className="btn btn-primary me-3">
                    Sign Up
                </Link>
                <Link to="/login" className="btn btn-secondary">
                    Log In
                </Link>
            </div>
        );
    }
    return (
        <div className="container text-center mt-5">
            <h1 className="mb-4">🏋️‍♂️ Welcome, {user.username}!</h1>
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