import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import AuthForm from "../components/AuthForm";
import { api } from "../services/api";

export default function LoginPage() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleLogin = async (payload) => {
    setLoading(true);
    setError("");
    try {
      const tokens = await api.login(payload);
      localStorage.setItem("accessToken", tokens.access_token);
      localStorage.setItem("refreshToken", tokens.refresh_token);
      navigate("/dashboard");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="page">
      <AuthForm type="login" onSubmit={handleLogin} loading={loading} />
      {error && <p className="error">{error}</p>}
      <p>
        No account yet? <Link to="/register">Register</Link>
      </p>
    </main>
  );
}
