import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import axiosInstance from "../api/axios";
import qs from "qs";

export default function SignUp() {
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [fullName, setFullName] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const { login } = useAuth();
    const navigate = useNavigate();

    const handleSignUp = async (e) => {
        e.preventDefault();
        setError("");

        try {
            // 1) Create the user
            await axiosInstance.post("/users/", {
                username,
                email,
                password,
                full_name: fullName || undefined,
            });

            // 2) Immediately log them in
            const res = await axiosInstance.post(
                "/users/token",
                qs.stringify({ username, password }),
                { headers: { "Content-Type": "application/x-www-form-urlencoded" } }
            );
            const token = res.data.access_token;
            login(token, { username });

            // 3) Redirect to Home
            navigate("/");
        } catch (err) {
            if (err.response?.status === 409) {
                setError("That username is already taken.");
            } else {
                setError(err.response?.data?.detail || "Sign up failed. Please try again.");
            }
        }
    };

    return (
        <div className="container mt-5" style={{ maxWidth: 400 }}>
            <h2 className="mb-4 text-center">Sign Up</h2>
            {error && <div className="alert alert-danger">{error}</div>}
            <form onSubmit={handleSignUp}>
                <input
                    className="form-control mb-2"
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                />
                <input
                    type="email"
                    className="form-control mb-2"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />
                <input
                    className="form-control mb-2"
                    placeholder="Full Name (optional)"
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                />
                <input
                    type="password"
                    className="form-control mb-3"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />
                <button className="btn btn-primary w-100" type="submit">
                    Create Account
                </button>
            </form>
            <p className="text-center mt-3">
                Already have an account?{" "}
                <Link to="/login">Log in here</Link>
            </p>
        </div>
    );
}