const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

export const tokenStorage = {
  get() {
    return localStorage.getItem("token") || "";
  },
  set(token) {
    localStorage.setItem("token", token);
  },
  clear() {
    localStorage.removeItem("token");
  }
};

async function apiFetch(path, options = {}) {
  const headers = new Headers(options.headers || {});
  const token = tokenStorage.get();
  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }
  let body = options.body;
  if (options.json) {
    headers.set("Content-Type", "application/json");
    body = JSON.stringify(options.json);
  }
  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
    body
  });
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || response.statusText);
  }
  if (response.status === 204) {
    return null;
  }
  return response.json();
}

export async function login(username, password) {
  const form = new URLSearchParams();
  form.set("username", username);
  form.set("password", password);
  const response = await fetch(`${API_BASE}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded"
    },
    body: form
  });
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || "Login failed");
  }
  return response.json();
}

export async function register(username, password) {
  const response = await fetch(`${API_BASE}/auth/register`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ username, password })
  });
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || "Registration failed");
  }
  return response.json();
}

export function fetchMe() {
  return apiFetch("/auth/me");
}

export function listQuizzes() {
  return apiFetch("/quizzes");
}

export function startAttempt(quizId) {
  return apiFetch(`/quizzes/${quizId}/attempts`, { method: "POST" });
}

export function getAttempt(attemptId) {
  return apiFetch(`/attempts/${attemptId}`);
}

export function submitAttempt(attemptId, answers) {
  return apiFetch(`/attempts/${attemptId}/submit`, {
    method: "POST",
    json: { answers }
  });
}

export function listUsers() {
  return apiFetch("/admin/users");
}

export function createUser(payload) {
  return apiFetch("/admin/users", { method: "POST", json: payload });
}

export function reloadSeed() {
  return apiFetch("/admin/seed/reload", { method: "POST" });
}
