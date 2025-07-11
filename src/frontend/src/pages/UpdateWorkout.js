import React, { useState, useEffect } from "react";
import Toast from "react-bootstrap/Toast";
import ToastContainer from "react-bootstrap/ToastContainer";
import axiosInstance from "../api/axios";
import { useAuth } from "../context/AuthContext";

const createDefaultSet = (set_number = 1) => ({ set_number, reps: 8, weight: 0 });

const createDefaultExercise = (exerciseName = "") => ({
    exercise: { name: exerciseName },
    sets: [createDefaultSet()],
});

function formatToDatetimeLocal(isoString) {
    const date = new Date(isoString);
    const tzOffset = date.getTimezoneOffset() * 60000;
    return new Date(date.getTime() - tzOffset).toISOString().slice(0, 16);
}

export default function UpdateWorkout() {
    const { user } = useAuth();
    const [workouts, setWorkouts] = useState([]);
    const [selectedWorkout, setSelectedWorkout] = useState(null);
    const [notes, setNotes] = useState("");
    const [createdTime, setCreatedTime] = useState(null);
    const [workoutType, setWorkoutType] = useState("");
    const [categories, setCategories] = useState([]);
    const [groupedExercises, setGroupedExercises] = useState({});
    const [toast, setToast] = useState({ show: false, message: "", variant: "info" });

    useEffect(() => {
        if (user?.username) {
            fetchWorkoutsByUser();
        }
    }, [user?.username]);

    useEffect(() => {
        axiosInstance.get("/exercises/categories")
            .then((res) => setCategories(Array.isArray(res.data) ? res.data : []))
            .catch(() => setCategories([]));

        axiosInstance.get("/exercises/categorized")
            .then((res) => setGroupedExercises(res.data || {}))
            .catch(() => setGroupedExercises({}));
    }, []);

    const showToast = (message, variant = "info") => {
        setToast({ show: true, message, variant });
        setTimeout(() => setToast({ show: false, message: "", variant: "info" }), 4000);
    };

    const fetchWorkoutsByUser = async () => {
        try {
            const res = await axiosInstance.get(`/workouts/user/${user.username}`);
            setWorkouts(Array.isArray(res.data) ? res.data : []);
        } catch {
            setWorkouts([]);
            showToast("Failed to fetch workouts", "danger");
        }
    };

    const handleSelectWorkout = (id) => {
        const workout = workouts.find((w) => w.id === id);
        if (!workout) return;
        const sortedLoggedExercises = (workout.logged_exercises || []).map((le) => ({
            ...le,
            sets: (le.sets || []).sort((a, b) => a.set_number - b.set_number),
        }));
        setSelectedWorkout({ ...workout, logged_exercises: sortedLoggedExercises });
        setNotes(workout.notes || "");
        setWorkoutType(workout.workout_type || "");
        setCreatedTime(workout.created_time || null);
    };

    const updateExerciseName = (exIndex, name) => {
        const updated = { ...selectedWorkout };
        updated.logged_exercises[exIndex].exercise.name = name;
        setSelectedWorkout(updated);
    };

    const updateSetValue = (exIndex, setIndex, field, value) => {
        const updatedWorkout = { ...selectedWorkout };
        updatedWorkout.logged_exercises[exIndex].sets[setIndex][field] = value;
        setSelectedWorkout(updatedWorkout);
    };

    const addSet = (exIndex) => {
        const updated = { ...selectedWorkout };
        const sets = updated.logged_exercises[exIndex].sets || [];
        sets.push(createDefaultSet(sets.length + 1));
        updated.logged_exercises[exIndex].sets = sets;
        setSelectedWorkout(updated);
    };

    const removeSet = (exIndex, setIndex) => {
        const updated = { ...selectedWorkout };
        const sets = updated.logged_exercises[exIndex].sets || [];
        updated.logged_exercises[exIndex].sets = sets.filter((_, i) => i !== setIndex);
        updated.logged_exercises[exIndex].sets.forEach((s, i) => (s.set_number = i + 1));
        setSelectedWorkout(updated);
    };

    const addExercise = () => {
        const updated = { ...selectedWorkout };
        updated.logged_exercises.push(createDefaultExercise());
        setSelectedWorkout(updated);
    };

    const removeExercise = (exIndex) => {
        const updated = { ...selectedWorkout };
        updated.logged_exercises = updated.logged_exercises.filter((_, i) => i !== exIndex);
        setSelectedWorkout(updated);
    };

    const handleUpdate = async () => {
        if (!selectedWorkout) return;

        const payload = {
            notes,
            created_time: createdTime ? formatToDatetimeLocal(createdTime) : undefined,
            workout_type: workoutType,
            logged_exercises: selectedWorkout.logged_exercises.map((le) => ({
                name: le.exercise.name,
                sets: le.sets.map((s) => ({
                    set_number: s.set_number,
                    reps: s.reps,
                    weight: s.weight,
                })),
            })),
        };

        try {
            await axiosInstance.patch(`/workouts/${selectedWorkout.id}`, payload);
            showToast("Workout updated successfully!", "success");
            await fetchWorkoutsByUser();
        } catch (err) {
            const details = err.response?.data?.detail;
            const msg = Array.isArray(details)
                ? details.map((d) => `${d.loc?.join(".")}: ${d.msg}`).join("; ")
                : typeof details === "string"
                    ? details
                    : "Unknown error";
            showToast("Update failed: " + msg, "danger");
        }
    };

    const handleDeleteWorkout = async () => {
        if (!selectedWorkout) return;
        try {
            await axiosInstance.delete(`/workouts/${selectedWorkout.id}`);
            showToast("Workout deleted successfully.", "success");
            setSelectedWorkout(null);
            setNotes("");
            setWorkoutType("");
            await fetchWorkoutsByUser();
        } catch {
            showToast("Failed to delete workout.", "danger");
        }
    };

    return (
        <div className="card p-4 position-relative">
            <ToastContainer className="position-absolute top-50 start-50 translate-middle" style={{ zIndex: 1060 }}>
                <Toast bg={toast.variant} show={toast.show} onClose={() => setToast({ ...toast, show: false })} delay={4000} autohide>
                    <Toast.Body className="text-white text-center">{toast.message}</Toast.Body>
                </Toast>
            </ToastContainer>

            <div className="mb-3">
                <select
                    className="form-select"
                    value={selectedWorkout?.id || ""}
                    onChange={(e) => handleSelectWorkout(e.target.value)}
                >
                    <option value="">Select a workout to edit</option>
                    {workouts.map((w) => (
                        <option key={w.id} value={w.id}>
                            {w.notes?.slice(0, 30) || "No notes"} — {w.workout_type}
                        </option>
                    ))}
                </select>
            </div>

            {selectedWorkout && (
                <>
                    <div className="mb-3">
                        <label>Workout Type</label>
                        <select
                            className="form-select"
                            value={workoutType}
                            onChange={(e) => setWorkoutType(e.target.value)}
                        >
                            <option value="">Select workout type</option>
                            {categories.map((type) => (
                                <option key={type} value={type}>{type}</option>
                            ))}
                        </select>
                    </div>

                    <div className="mb-3">
                        <label>Date &amp; Time</label>
                        <input
                            type="datetime-local"
                            className="form-control"
                            value={createdTime}
                            onChange={(e) => setCreatedTime(e.target.value)}
                        />
                    </div>

                    <div className="mb-3">
                        <label>Notes</label>
                        <textarea
                            className="form-control"
                            value={notes}
                            onChange={(e) => setNotes(e.target.value)}
                        />
                    </div>

                    {selectedWorkout.logged_exercises.map((ex, exIndex) => (
                        <div key={exIndex} className="border p-3 mb-4 rounded">
                            <div className="d-flex justify-content-between align-items-center mb-2">
                                <h6 className="mb-0">Exercise {exIndex + 1}</h6>
                                <button className="btn btn-sm btn-outline-danger" onClick={() => removeExercise(exIndex)}>
                                    Remove
                                </button>
                            </div>

                            <select
                                className="form-select mb-3"
                                value={ex.exercise.name}
                                onChange={(e) => updateExerciseName(exIndex, e.target.value)}
                            >
                                <option value="">Select an exercise</option>
                                {Object.entries(groupedExercises).map(([group, exercises]) => (
                                    <optgroup key={group} label={group}>
                                        {exercises.map((exercise) => (
                                            <option key={exercise.id} value={exercise.name}>
                                                {exercise.name}
                                            </option>
                                        ))}
                                    </optgroup>
                                ))}
                            </select>

                            <div className="row fw-bold mb-2">
                                <div className="col-2">Set #</div>
                                <div className="col-5">Reps</div>
                                <div className="col-5">Weight (lb)</div>
                            </div>

                            {ex.sets.map((set, setIndex) => (
                                <div key={setIndex} className="row mb-2 align-items-center">
                                    <div className="col-2">{set.set_number}</div>
                                    <div className="col-5">
                                        <input
                                            type="number"
                                            className="form-control"
                                            value={set.reps}
                                            onChange={(e) => updateSetValue(exIndex, setIndex, "reps", parseInt(e.target.value))}
                                        />
                                    </div>
                                    <div className="col-5 d-flex">
                                        <input
                                            type="number"
                                            className="form-control me-2"
                                            value={set.weight}
                                            onChange={(e) => updateSetValue(exIndex, setIndex, "weight", parseFloat(e.target.value))}
                                        />
                                        <button
                                            className="btn btn-sm btn-outline-danger"
                                            onClick={() => removeSet(exIndex, setIndex)}
                                        >
                                            ×
                                        </button>
                                    </div>
                                </div>
                            ))}

                            <button className="btn btn-sm btn-outline-primary mt-2" onClick={() => addSet(exIndex)}>
                                + Add Set
                            </button>
                        </div>
                    ))}

                    <button className="btn btn-outline-primary mb-3" onClick={addExercise}>
                        + Add Exercise
                    </button>

                    <div className="d-flex gap-3">
                        <button className="btn btn-primary" onClick={handleUpdate}>
                            Submit Update
                        </button>
                        <button className="btn btn-danger" onClick={handleDeleteWorkout}>
                            Delete Workout
                        </button>
                    </div>
                </>
            )}
        </div>
    );
}