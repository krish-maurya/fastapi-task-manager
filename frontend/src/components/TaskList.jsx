import React, { useState } from "react";

export default function TaskList({ tasks, onUpdate, onDelete }) {
  const [editingId, setEditingId] = useState(null);
  const [editTitle, setEditTitle] = useState("");
  const [editDescription, setEditDescription] = useState("");

  const startEdit = (task) => {
    setEditingId(task.id);
    setEditTitle(task.title);
    setEditDescription(task.description || "");
  };

  const saveEdit = () => {
    onUpdate(editingId, { title: editTitle, description: editDescription });
    setEditingId(null);
  };

  if (!tasks.length) {
    return <p className="card">No tasks yet. Create your first task.</p>;
  }

  return (
    <div className="grid">
      {tasks.map((task) => (
        <div key={task.id} className="card">
          {editingId === task.id ? (
            <>
              <input value={editTitle} onChange={(e) => setEditTitle(e.target.value)} />
              <textarea value={editDescription} onChange={(e) => setEditDescription(e.target.value)} />
              <div className="actions">
                <button onClick={saveEdit}>Save</button>
                <button className="secondary" onClick={() => setEditingId(null)}>
                  Cancel
                </button>
              </div>
            </>
          ) : (
            <>
              <h4>{task.title}</h4>
              <p>{task.description || "No description"}</p>
              <small>Owner ID: {task.owner_id}</small>
              <div className="actions">
                <button onClick={() => startEdit(task)}>Edit</button>
                <button className="danger" onClick={() => onDelete(task.id)}>
                  Delete
                </button>
              </div>
            </>
          )}
        </div>
      ))}
    </div>
  );
}
