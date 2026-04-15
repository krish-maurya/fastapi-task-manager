const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1";

function getHeaders(includeAuth = false) {
  const headers = { "Content-Type": "application/json" };
  if (includeAuth) {
    const token = localStorage.getItem("accessToken");
    if (token) {
      headers.Authorization = `Bearer ${token}`;
    }
  }
  return headers;
}

async function request(path, options = {}, includeAuth = false) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      ...getHeaders(includeAuth),
      ...(options.headers || {}),
    },
  });

  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(data.detail || "Something went wrong");
  }
  return data;
}

export const api = {
  register: (payload) =>
    request("/auth/register", {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  login: (payload) =>
    request("/auth/login", {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  refresh: (refreshToken) =>
    request("/auth/refresh", {
      method: "POST",
      body: JSON.stringify({ refresh_token: refreshToken }),
    }),

  getTasks: () => request("/tasks", { method: "GET" }, true),

  createTask: (payload) =>
    request(
      "/tasks",
      {
        method: "POST",
        body: JSON.stringify(payload),
      },
      true
    ),

  updateTask: (id, payload) =>
    request(
      `/tasks/${id}`,
      {
        method: "PUT",
        body: JSON.stringify(payload),
      },
      true
    ),

  deleteTask: (id) => request(`/tasks/${id}`, { method: "DELETE" }, true),
};
