import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import axiosInstance from "../api/axios";
import qs from "qs";

export default function Login() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const { login } = useAuth();
    const navigate = useNavigate();

    const handleLogin = async () => {
        try {
            const res = await axiosInstance.post(
                "/users/token",
                qs.stringify({ username, password }),
                { headers: { "Content-Type": "application/x-www-form-urlencoded" } }
            );
            const token = res.data.access_token;
            login(token, { username });
            navigate("/");
        } catch (err) {
            console.error("Login failed", err);
            setError("Invalid login credentials");
        }
    };

    return (
        <div className="container mt-5">
            <h2>Login</h2>
            {error && <div className="alert alert-danger">{error}</div>}
            <input
                className="form-control mb-2"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
            />
            <input
                type="password"
                className="form-control mb-2"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            />
            <button className="btn btn-primary" onClick={handleLogin}>
                Log In
            </button>
        </div>
    );
}