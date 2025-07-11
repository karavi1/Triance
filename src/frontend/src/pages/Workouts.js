import React, { useState } from "react";
import { useAuth } from "../context/AuthContext";
import axiosInstance from "../api/axios";
import { Tabs, Tab } from "react-bootstrap";

import CreateWorkout from "./CreateWorkout";
import UpdateWorkout from "./UpdateWorkout";

export default function Workouts() {
    const { user } = useAuth();
    const username = user?.username;

    const [type, setType] = useState("Push");
    const [allWorkouts, setAllWorkouts] = useState([]);
    const [singleWorkout, setSingleWorkout] = useState(null);
    const [message, setMessage] = useState("");
    const [tabKey, setTabKey] = useState("all");

    const [expandedWorkouts, setExpandedWorkouts] = useState({});

    const fetchAllByUser = async () => {
        if (!username) return setMessage("You must be logged in to see workouts");
        try {
            const res = await axiosInstance.get(`/workouts/user/${username}`);
            const data = res.data;
            setAllWorkouts(Array.isArray(data) ? data : []);
            setSingleWorkout(null);
            setMessage(!Array.isArray(data) || data.length === 0
                ? "No workouts found for you"
                : ""
            );
        } catch (err) {
            console.error(err);
            setAllWorkouts([]);
            setMessage("Failed to fetch your workouts");
        }
    };

    const fetchLatestByUser = async () => {
        if (!username) return setMessage("You must be logged in to see workouts");
        try {
            const res = await axiosInstance.get(`/workouts/user/${username}/latest`);
            setSingleWorkout(res.data || null);
            setAllWorkouts([]);
            setMessage(!res.data ? "No latest workout found" : "");
        } catch (err) {
            console.error(err);
            setSingleWorkout(null);
            setMessage("Failed to fetch your latest workout");
        }
    };

    const fetchLatestByUserAndType = async () => {
        if (!username) return setMessage("You must be logged in to see workouts");
        try {
            const res = await axiosInstance.get(
                `/workouts/user/${username}/latest/${type}`
            );
            setSingleWorkout(res.data || null);
            setAllWorkouts([]);
            setMessage(!res.data
                ? `No ${type} workout found`
                : ""
            );
        } catch (err) {
            console.error(err);
            setSingleWorkout(null);
            setMessage(`Failed to fetch latest ${type} workout`);
        }
    };

    const toggleExpand = async (workoutId) => {
        if (expandedWorkouts[workoutId]) {
            setExpandedWorkouts(prev => {
                const copy = { ...prev };
                delete copy[workoutId];
                return copy;
            });
        } else {
            try {
                const res = await axiosInstance.get(`/workouts/${workoutId}`);
                setExpandedWorkouts(prev => ({
                    ...prev,
                    [workoutId]: res.data
                }));
            } catch (err) {
                console.error(`Failed to fetch workout ${workoutId}`, err);
                setMessage("Error loading workout details");
            }
        }
    };

    return (
        <div className="container mt-5 mb-5">
            <h2 className="mb-4">Workout Manager</h2>

            {message && (
                <div className="alert alert-info">{message}</div>
            )}

            <div className="btn-toolbar mb-4" role="toolbar">
                <div className="btn-group me-2" role="group">
                    <button
                        className="btn btn-outline-primary"
                        onClick={fetchAllByUser}
                        disabled={!username}
                    >
                        All Workouts
                    </button>
                    <button
                        className="btn btn-outline-secondary"
                        onClick={fetchLatestByUser}
                        disabled={!username}
                    >
                        Latest Workout
                    </button>
                </div>
                <div className="input-group" role="group">
                    <select
                        className="form-select"
                        value={type}
                        onChange={(e) => setType(e.target.value)}
                    >
                        {["Push","Pull","Quads","Hams","Upper","Lower","Full Body","Custom"]
                            .map((t) => (
                                <option key={t} value={t}>{t}</option>
                            ))
                        }
                    </select>
                    <button
                        className="btn btn-outline-success"
                        onClick={fetchLatestByUserAndType}
                        disabled={!username}
                    >
                        Latest by Type
                    </button>
                </div>
            </div>

            {allWorkouts.length > 0 && allWorkouts.map((w, i) => (
                <div key={w.id} className="card p-3 mb-3">
                    <div className="d-flex justify-content-between align-items-center">
                        <p className="mb-0">
                            <strong>#{i + 1}</strong> {w.workout_type} –{" "}
                            {new Date(w.created_time).toLocaleString()}
                        </p>
                        <button
                            className="btn btn-sm btn-outline-info"
                            onClick={() => toggleExpand(w.id)}
                        >
                            {expandedWorkouts[w.id] ? "Collapse" : "Expand"}
                        </button>
                    </div>

                    {expandedWorkouts[w.id] && (
                        <div className="mt-3 border-top pt-3">
                            <p>
                                <strong>Type:</strong> {expandedWorkouts[w.id].workout_type}
                            </p>
                            <p>
                                <strong>Notes:</strong> {expandedWorkouts[w.id].notes || "None"}
                            </p>
                            <div className="table-responsive">
                                {Array.isArray(expandedWorkouts[w.id].logged_exercises) &&
                                    expandedWorkouts[w.id].logged_exercises.map((le, idx) => (
                                        <div key={idx} className="mb-3">
                                            <h6>{le.exercise_name || le.exercise?.name}</h6>
                                            <table className="table table-sm">
                                                <thead>
                                                    <tr>
                                                        <th>Set</th>
                                                        <th>Reps</th>
                                                        <th>Weight</th>
                                                    </tr>
                                                </thead>
                                                <tbody>
                                                    {le.sets
                                                        .slice()
                                                        .sort((a, b) => a.set_number - b.set_number)
                                                        .map((s) => (
                                                            <tr key={s.set_number}>
                                                                <td>{s.set_number}</td>
                                                                <td>{s.reps}</td>
                                                                <td>{s.weight}</td>
                                                            </tr>
                                                        ))
                                                    }
                                                </tbody>
                                            </table>
                                        </div>
                                    ))
                                }
                            </div>
                        </div>
                    )}
                </div>
            ))}

            {singleWorkout && (
                <div className="card p-3 mb-4">
                    <h5>Workout Details</h5>
                    <p>
                        <strong>Type:</strong> {singleWorkout.workout_type}
                    </p>
                    <p>
                        <strong>Notes:</strong> {singleWorkout.notes || "None"}
                    </p>
                    <p>
                        <strong>Date:</strong>{" "}
                        {new Date(singleWorkout.created_time).toLocaleString()}
                    </p>
                    <div className="table-responsive mt-3">
                        {Array.isArray(singleWorkout.logged_exercises) &&
                            singleWorkout.logged_exercises.map((le, idx) => (
                                <div key={idx} className="mb-3">
                                    <h6>{le.exercise_name || le.exercise?.name}</h6>
                                    <table className="table table-sm">
                                        <thead>
                                            <tr>
                                                <th>Set</th>
                                                <th>Reps</th>
                                                <th>Weight</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {le.sets
                                                .slice()
                                                .sort((a, b) => a.set_number - b.set_number)
                                                .map((s) => (
                                                    <tr key={s.set_number}>
                                                        <td>{s.set_number}</td>
                                                        <td>{s.reps}</td>
                                                        <td>{s.weight}</td>
                                                    </tr>
                                                ))
                                            }
                                        </tbody>
                                    </table>
                                </div>
                            ))
                        }
                    </div>
                </div>
            )}

            <Tabs
                id="workout-tabs"
                activeKey={tabKey}
                onSelect={(k) => setTabKey(k)}
                className="mt-4"
            >
                <Tab eventKey="create" title="➕ Create Workout">
                    <CreateWorkout />
                </Tab>
                <Tab eventKey="update" title="✏️ Update Workout">
                    <UpdateWorkout />
                </Tab>
            </Tabs>
        </div>
    );
}