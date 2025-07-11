import React, { useEffect, useState } from "react";
import axiosInstance from "../api/axios";
import { Modal, Button, Form } from "react-bootstrap";

export default function Exercises() {
    const [exercises, setExercises] = useState([]);
    const [groupedExercises, setGroupedExercises] = useState({});
    const [showGrouped, setShowGrouped] = useState(true);

    const [name, setName] = useState("");
    const [description, setDescription] = useState("");
    const [primaryMuscles, setPrimaryMuscles] = useState("");
    const [secondaryMuscles, setSecondaryMuscles] = useState("");
    const [categories, setCategories] = useState([]);
    const [selectedCategory, setSelectedCategory] = useState("");

    const [exerciseId, setExerciseId] = useState("");
    const [updatedName, setUpdatedName] = useState("");
    const [updatedDescription, setUpdatedDescription] = useState("");

    const [updateMessage, setUpdateMessage] = useState("");
    const [deleteMessage, setDeleteMessage] = useState("");

    const [showModal, setShowModal] = useState(false);

    const fetchAll = async () => {
        try {
            const res = await axiosInstance.get("/exercises/");
            setExercises(res.data);
        } catch (err) {
            console.error("Failed to fetch exercises", err);
        }
    };

    const fetchGrouped = async () => {
        try {
            const res = await axiosInstance.get("/exercises/categorized");
            setGroupedExercises(res.data);
        } catch (err) {
            console.error("Failed to fetch categorized exercises", err);
        }
    };

    const fetchCategories = async () => {
        try {
            const res = await axiosInstance.get("/exercises/categories");
            setCategories(res.data);
            if (res.data.length > 0) setSelectedCategory(res.data[0]);
        } catch (err) {
            console.error("Failed to load categories", err);
        }
    };

    const createExercise = async () => {
        try {
            await axiosInstance.post("/exercises/", {
                name,
                description,
                category: selectedCategory,
                primary_muscles: [primaryMuscles],
                secondary_muscles: secondaryMuscles
                    .split(",")
                    .map((s) => s.trim())
                    .filter((s) => s),
            });
            setName("");
            setDescription("");
            setPrimaryMuscles("core");
            setSelectedCategory(categories[0] || "");
            fetchAll();
            fetchGrouped();
        } catch (err) {
            console.error("Create failed", err);
        }
    };

    const updateExercise = async () => {
        try {
            await axiosInstance.patch(`/exercises/${exerciseId}`, {
                name: updatedName,
                description: updatedDescription,
            });
            setUpdateMessage("Updated successfully!");
            setShowModal(false);
            fetchAll();
            fetchGrouped();
        } catch (err) {
            console.error("Update failed", err);
            setUpdateMessage("Update failed.");
        }
    };

    const deleteExercise = async () => {
        try {
            await axiosInstance.delete(`/exercises/${exerciseId}`);
            setDeleteMessage("Deleted successfully!");
            fetchAll();
            fetchGrouped();
        } catch (err) {
            console.error("Delete failed", err);
            setDeleteMessage("Delete failed.");
        }
    };

    useEffect(() => {
        fetchAll();
        fetchGrouped();
        fetchCategories();
    }, []);

    const handleOpenModal = () => {
        const ex = exercises.find((e) => e.id === exerciseId);
        if (ex) {
            setUpdatedName(ex.name);
            setUpdatedDescription(ex.description || "");
            setShowModal(true);
        }
    };

    return (
        <div className="container mt-5 mb-5">
            <h2 className="mb-4">Exercise Manager</h2>

            <div className="card p-4 mb-4">
                <h5 className="mb-3">Create New Exercise</h5>
                <input
                    className="form-control mb-2"
                    placeholder="Exercise Name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                />
                <input
                    className="form-control mb-2"
                    placeholder="Description"
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                />
                <input
                    className="form-control mb-2"
                    placeholder="Primary Muscle Group"
                    value={primaryMuscles}
                    onChange={(e) => setPrimaryMuscles(e.target.value)}
                />
                <input
                    className="form-control mb-3"
                    placeholder="Secondary Muscles (comma-separated)"
                    value={secondaryMuscles}
                    onChange={(e) => setSecondaryMuscles(e.target.value)}
                />
                <select
                    className="form-select mb-3"
                    value={selectedCategory}
                    onChange={(e) => setSelectedCategory(e.target.value)}
                >
                    {categories.map((cat) => (
                        <option key={cat} value={cat}>{cat}</option>
                    ))}
                </select>
                <button className="btn btn-primary" onClick={createExercise}>
                    Create
                </button>
            </div>

            <div className="card p-4 mb-4">
                <h5 className="mb-3">Update Exercise</h5>
                <select
                    className="form-select mb-3"
                    value={exerciseId}
                    onChange={(e) => setExerciseId(e.target.value)}
                >
                    <option value="">Select an exercise</option>
                    {Object.entries(groupedExercises).map(([category, exerciseList]) => (
                        <optgroup key={category} label={category}>
                            {exerciseList.map((exercise) => (
                                <option key={exercise.id} value={exercise.id}>
                                    {exercise.name}
                                </option>
                            ))}
                        </optgroup>
                    ))}
                </select>
                <button
                    className="btn btn-warning text-white"
                    onClick={handleOpenModal}
                    disabled={!exerciseId}
                >
                    Update Selected Exercise
                </button>
                {updateMessage && (
                    <div className="mt-2 alert alert-info">{updateMessage}</div>
                )}
            </div>

            {/* Delete */}
            <div className="card p-4 mb-4">
                <h5 className="mb-3">Delete Exercise</h5>
                <select
                    className="form-select mb-3"
                    value={exerciseId}
                    onChange={(e) => setExerciseId(e.target.value)}
                >
                    <option value="">Select an exercise</option>
                    {Object.entries(groupedExercises).map(([category, exerciseList]) => (
                        <optgroup key={category} label={category}>
                            {exerciseList.map((exercise) => (
                                <option key={exercise.id} value={exercise.id}>
                                    {exercise.name}
                                </option>
                            ))}
                        </optgroup>
                    ))}
                </select>
                <button
                    className="btn btn-danger"
                    onClick={deleteExercise}
                    disabled={!exerciseId}
                >
                    Delete Selected Exercise
                </button>
                {deleteMessage && (
                    <div className="mt-2 alert alert-warning">{deleteMessage}</div>
                )}
            </div>

            {/* Modal */}
            <Modal show={showModal} onHide={() => setShowModal(false)}>
                <Modal.Header closeButton>
                    <Modal.Title>Edit Exercise</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Form.Group className="mb-3">
                        <Form.Label>Exercise Name</Form.Label>
                        <Form.Control
                            type="text"
                            value={updatedName}
                            onChange={(e) => setUpdatedName(e.target.value)}
                        />
                    </Form.Group>
                    <Form.Group className="mb-3">
                        <Form.Label>Description</Form.Label>
                        <Form.Control
                            type="text"
                            value={updatedDescription}
                            onChange={(e) => setUpdatedDescription(e.target.value)}
                        />
                    </Form.Group>
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={() => setShowModal(false)}>
                        Cancel
                    </Button>
                    <Button variant="success" onClick={updateExercise}>
                        Save Changes
                    </Button>
                </Modal.Footer>
            </Modal>

            <div className="card p-4">
                <h5 className="mb-3">{showGrouped ? "Exercises by Category" : "All Exercises"}</h5>
                <div className="mb-3">
                    <button
                        className="btn btn-outline-secondary"
                        onClick={() => setShowGrouped(!showGrouped)}
                    >
                        {showGrouped ? "Show Flat List" : "Show Grouped by Category"}
                    </button>
                </div>
                {showGrouped ? (
                    Object.entries(groupedExercises).map(([category, group]) => (
                        <div key={category} className="mb-4">
                            <h6 className="text-primary">{category}</h6>
                            <ul className="list-group">
                                {group.map((ex) => (
                                    <li
                                        key={ex.id}
                                        className="list-group-item d-flex justify-content-between align-items-center"
                                    >
                                        <div>
                                            <strong>{ex.name}</strong>
                                            <div className="text-muted small">
                                                {ex.description || "No description"}
                                            </div>
                                        </div>
                                        <span className="badge bg-secondary">{ex.id.slice(0, 6)}...</span>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    ))
                ) : (
                    <ul className="list-group">
                        {exercises.map((ex) => (
                            <li
                                key={ex.id}
                                className="list-group-item d-flex justify-content-between align-items-center"
                            >
                                <div>
                                    <strong>{ex.name}</strong>
                                    <div className="text-muted small">
                                        {ex.description || "No description"}
                                    </div>
                                </div>
                                <span className="badge bg-secondary">{ex.id.slice(0, 6)}...</span>
                            </li>
                        ))}
                    </ul>
                )}
            </div>
        </div>
    );
}