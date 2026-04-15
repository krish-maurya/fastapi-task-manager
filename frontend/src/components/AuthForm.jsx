import React, { useState } from "react";

export default function AuthForm({ type, onSubmit, loading }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("user");

  const isRegister = type === "register";

  const handleSubmit = (event) => {
    event.preventDefault();
    onSubmit({ email, password, ...(isRegister ? { role } : {}) });
  };

  return (
    <form className="card form" onSubmit={handleSubmit}>
      <h2>{isRegister ? "Create account" : "Sign in"}</h2>
      <label>
        Email
        <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
      </label>
      <label>
        Password
        <input
          type="password"
          minLength={8}
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
      </label>
      {isRegister && (
        <label>
          Role
          <select value={role} onChange={(e) => setRole(e.target.value)}>
            <option value="user">User</option>
            <option value="admin">Admin</option>
          </select>
        </label>
      )}
      <button type="submit" disabled={loading}>
        {loading ? "Please wait..." : isRegister ? "Register" : "Login"}
      </button>
    </form>
  );
}
