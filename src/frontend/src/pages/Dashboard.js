import React, { useEffect, useState } from "react";
import { Bar } from "react-chartjs-2";
import { Chart as ChartJS, BarElement, CategoryScale, LinearScale, Tooltip, Legend } from "chart.js";

ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend);

export default function Dashboard() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    // Dummy data to simulate backend response
    const dummyStats = {
      total_workouts: 18,
      workouts_by_type: {
        Push: 5,
        Pull: 4,
        Quads: 3,
        Hams: 2,
        "Full Body": 2,
        Custom: 2
      },
      avg_sets_per_workout: 7.6,
      avg_reps_per_set: 10.1,
      most_common_exercises: ["Squat", "Deadlift", "Dips", "Incline DB Bench", "Lat Pulldown"]
    };

    setStats(dummyStats);
  }, []);

  if (!stats) return <div className="text-muted mt-5">Loading dashboard...</div>;

  const chartData = {
    labels: Object.keys(stats.workouts_by_type),
    datasets: [
      {
        label: "Workouts",
        data: Object.values(stats.workouts_by_type),
        backgroundColor: "rgba(54, 162, 235, 0.6)",
        borderRadius: 6
      }
    ]
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: { display: false }
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: { stepSize: 1 }
      }
    }
  };

  return (
    <div className="container mt-5 mb-5">
      <h2 className="mb-4">📊 (Dummy) Workout Dashboard</h2>

      {/* Stat Cards */}
      <div className="row mb-4">
        <div className="col-md-4">
          <div className="card bg-primary text-white mb-3 shadow-sm">
            <div className="card-body">
              <h5 className="card-title">Total Workouts</h5>
              <p className="fs-4">{stats.total_workouts}</p>
            </div>
          </div>
        </div>
        <div className="col-md-4">
          <div className="card bg-success text-white mb-3 shadow-sm">
            <div className="card-body">
              <h5 className="card-title">Avg Sets / Workout</h5>
              <p className="fs-4">{stats.avg_sets_per_workout.toFixed(1)}</p>
            </div>
          </div>
        </div>
        <div className="col-md-4">
          <div className="card bg-info text-white mb-3 shadow-sm">
            <div className="card-body">
              <h5 className="card-title">Avg Reps / Set</h5>
              <p className="fs-4">{stats.avg_reps_per_set.toFixed(1)}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Chart */}
      <div className="card p-4 mb-4 shadow-sm">
        <h5 className="mb-3">Workouts by Type</h5>
        <Bar data={chartData} options={chartOptions} />
      </div>

      {/* Common Exercises */}
      <div className="card p-4 shadow-sm">
        <h5 className="mb-3">Most Common Exercises</h5>
        <ul className="list-group">
          {stats.most_common_exercises.map((ex, idx) => (
            <li key={idx} className="list-group-item">
              {ex}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}