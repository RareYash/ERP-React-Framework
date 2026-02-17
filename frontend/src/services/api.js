/**
 * API Service Layer
 * Centralised HTTP client for the FastAPI backend.
 */

const API_BASE = "";

/**
 * Get the stored JWT token.
 */
export function getToken() {
  return localStorage.getItem("access_token");
}

/**
 * Store authentication data after login.
 */
export function setAuth(data) {
  localStorage.setItem("access_token", data.access_token);
  localStorage.setItem("user", JSON.stringify({
    username: data.username,
    role: data.role,
    student_id: data.student_id,
  }));
}

/**
 * Clear authentication data on logout.
 */
export function clearAuth() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("user");
}

/**
 * Get the current user object from storage.
 */
export function getUser() {
  const raw = localStorage.getItem("user");
  return raw ? JSON.parse(raw) : null;
}

/**
 * Authenticated fetch wrapper — auto-attaches the Bearer token.
 * Throws on non-OK responses with the server error detail.
 */
async function apiFetch(path, options = {}) {
  const token = getToken();
  const headers = {
    "Content-Type": "application/json",
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...options.headers,
  };

  const res = await fetch(`${API_BASE}${path}`, { ...options, headers });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    const error = new Error(err.detail || "Request failed");
    error.status = res.status;
    throw error;
  }

  return res.json();
}

// -------------------------------------------------------------------
// Auth endpoints
// -------------------------------------------------------------------
export async function login(username, password) {
  return apiFetch("/api/auth/login", {
    method: "POST",
    body: JSON.stringify({ username, password }),
  });
}

// -------------------------------------------------------------------
// Student endpoints
// -------------------------------------------------------------------
export async function fetchStudents() {
  return apiFetch("/api/students/");
}

export async function fetchStudent(id) {
  return apiFetch(`/api/students/${id}`);
}

export async function fetchStudentSummary(id) {
  return apiFetch(`/api/students/${id}/summary`);
}

export async function fetchIndividualReviews(id) {
  return apiFetch(`/api/students/${id}/reviews`);
}

export async function addReview(studentId, reviewText, teacherName = "Teacher") {
  return apiFetch(`/api/students/${studentId}/review`, {
    method: "POST",
    body: JSON.stringify({ review_text: reviewText, teacher_name: teacherName }),
  });
}

export async function updateReview(studentId, reviewText) {
  return apiFetch(`/api/students/${studentId}/review`, {
    method: "PUT",
    body: JSON.stringify({ review_text: reviewText }),
  });
}

export async function searchStudents(query) {
  return apiFetch(`/api/students/search/${encodeURIComponent(query)}`);
}

export async function updateStudentDetails(studentId, details) {
  return apiFetch(`/api/students/${studentId}/details`, {
    method: "PUT",
    body: JSON.stringify(details),
  });
}

export async function sentimentPreview(text) {
  return apiFetch("/api/students/sentiment-preview", {
    method: "POST",
    body: JSON.stringify({ review_text: text }),
  });
}

// -------------------------------------------------------------------
// Analytics endpoints
// -------------------------------------------------------------------
export async function fetchClassAnalytics() {
  return apiFetch("/api/analytics/class");
}

export async function fetchGradeAnalytics() {
  return apiFetch("/api/analytics/grades");
}

export async function fetchFilters() {
  return apiFetch("/api/analytics/filters");
}

// -------------------------------------------------------------------
// Chat (AI Assistant)
// -------------------------------------------------------------------
export async function sendChatMessage(message, history = []) {
  return apiFetch("/api/chat", {
    method: "POST",
    body: JSON.stringify({ message, history }),
  });
}
