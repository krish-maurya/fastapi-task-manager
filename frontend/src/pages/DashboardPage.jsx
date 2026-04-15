import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import TaskForm from "../components/TaskForm";
import TaskList from "../components/TaskList";
import { api } from "../services/api";

export default function DashboardPage() {
  const navigate = useNavigate();
  const [tasks, setTasks] = useState([]);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const loadTasks = async () => {
    setError("");
    try {
      const data = await api.getTasks();
      setTasks(data);
    } catch (err) {
      setError(err.message);
    }
  };

  useEffect(() => {
    loadTasks();
  }, []);

  const handleCreate = async (payload) => {
    setMessage("");
    setError("");
    try {
      await api.createTask(payload);
      setMessage("Task created");
      await loadTasks();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleUpdate = async (id, payload) => {
    setMessage("");
    setError("");
    try {
      await api.updateTask(id, payload);
      setMessage("Task updated");
      await loadTasks();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleDelete = async (id) => {
    setMessage("");
    setError("");
    try {
      await api.deleteTask(id);
      setMessage("Task deleted");
      await loadTasks();
    } catch (err) {
      setError(err.message);
    }
  };

  const logout = () => {
    localStorage.removeItem("accessToken");
    localStorage.removeItem("refreshToken");
    navigate("/login");
  };

  return (
    <main className="page">
      <header className="topbar">
        <h1>Task Dashboard</h1>
        <button className="secondary" onClick={logout}>
          Logout
        </button>
      </header>

      <TaskForm onCreate={handleCreate} />
      {message && <p className="success">{message}</p>}
      {error && <p className="error">{error}</p>}
      <TaskList tasks={tasks} onUpdate={handleUpdate} onDelete={handleDelete} />
    </main>
  );
}
