// src/api/api.jsx
const API_URL = "http://localhost:8000"; 
// Ajuste se estiver usando outro endereço

// === Função genérica para requisições ===
async function request(endpoint, method = "GET", body = null, token = null) {
  const headers = { "Content-Type": "application/json" };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const options = { method, headers };

  if (body) {
    options.body = JSON.stringify(body);
  }

  const res = await fetch(`${API_URL}${endpoint}`, options);

  if (!res.ok) {
    const errorText = await res.text();
    throw new Error(`Erro na API: ${res.status} - ${errorText}`);
  }

  return res.json();
}

// =======================
// AUTH
// =======================
export async function login(username, password) {
  return request("/auth/login", "POST", { username, password });
}

// =======================
// CHECK - Nova checagem
// =======================
export async function sendCheck(text, token) {
  return request("/check", "POST", { text }, token);
}

// =======================
// HISTORY
// =======================
export async function getHistory(token) {
  return request("/history", "GET", null, token);
}

export async function getHistoryItem(id, token) {
  return request(`/history/${id}`, "GET", null, token);
}

export async function deleteHistoryItem(id, token) {
  return request(`/history/${id}`, "DELETE", null, token);
}

export async function clearHistory(token) {
  return request("/history/clear", "DELETE", null, token);
}

