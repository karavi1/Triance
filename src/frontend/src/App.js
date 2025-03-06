import React, { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [message, setMessage] = useState("");

  useEffect(() => {
    axios.get("http://18.119.104.96:8000/docs")  // Adjust to your actual backend URL
      .then(response => setMessage(response.data.message))
      .catch(error => console.error("Error fetching API:", error));
  }, []);

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h1>Fitness Tracker</h1>
      <p>{message}</p>
    </div>
  );
}

export default App;
