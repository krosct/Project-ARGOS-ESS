const API_URL = "http://localhost:8000"; // ajuste se necessário

// === Função genérica de requisição ===
async function request(endpoint, method = "GET", body = null, token = null) {
  const headers = { "Content-Type": "application/json" };

  if (token) headers["Authorization"] = `Bearer ${token}`;

  const options = { method, headers };

  if (body) options.body = JSON.stringify(body);

  const res = await fetch(`${API_URL}${endpoint}`, options);

  if (!res.ok) {
    const errorText = await res.text();
    throw new Error(`Erro na API: ${res.status} - ${errorText}`);
  }

  return res.json();
}

// =======================
// AUTENTICAÇÃO
// =======================
export async function login(username, password) {
  return request("/auth/login", "POST", { username, password });
}

// =======================
// CHECAGEM DE FAKE NEWS
// =======================

// Envia uma nova checagem
export async function submitCheck(text, token = null) {
  return request("/check", "POST", { text }, token);
}

// Consulta o status de uma checagem existente
export async function getCheckStatus(id, token = null) {
  return request(`/check/${id}`, "GET", null, token);
}

// =======================
// HISTÓRICO
// =======================

// Lista todo o histórico
export async function getHistory(token = null) {
  return request("/history", "GET", null, token);
}

// Pega um item específico do histórico
export async function getHistoryItem(id, token = null) {
  return request(`/history/${id}`, "GET", null, token);
}

// Deleta um item específico
export async function deleteHistoryItem(id, token = null) {
  return request(`/history/${id}`, "DELETE", null, token);
}

// Limpa todo o histórico
export async function clearHistory(token = null) {
  return request("/history/clear", "DELETE", null, token);
}
