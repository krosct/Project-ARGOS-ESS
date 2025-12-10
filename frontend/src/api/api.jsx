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
    let errorMessage = `Erro na API: ${res.status}`;
    try {
      const errorJson = JSON.parse(errorText);
      errorMessage = errorJson.detail || errorMessage;
    } catch {
      errorMessage = errorText || errorMessage;
    }
    throw new Error(errorMessage);
  }

  return res.json();
}

// =======================
// AUTENTICAÇÃO
// =======================
export async function login(username, password) {
  return request("/api/auth/login", "POST", { username, password });
}

// =======================
// CHECAGEM DE FAKE NEWS
// =======================

// Envia uma nova checagem (aceita text ou url)
export async function submitCheck({ text, url } = {}, token = null) {
  const body = {};
  if (text) body.text = text;
  if (url) body.url = url;
  return request("/api/check/", "POST", body, token);
}

// Consulta o status de uma checagem existente
export async function getCheckStatus(id, token = null) {
  return request(`/api/check/${id}`, "GET", null, token);
}

// =======================
// HISTÓRICO
// =======================

// Lista todo o histórico
export async function getHistory(token = null) {
  return request("/api/history", "GET", null, token);
}

// Pega um item específico do histórico
export async function getHistoryItem(id, token = null) {
  return request(`/api/history/${id}`, "GET", null, token);
}

// Deleta um item específico
export async function deleteHistoryItem(id, token = null) {
  return request(`/api/history/${id}`, "DELETE", null, token);
}

// Limpa todo o histórico
export async function clearHistory(token = null) {
  return request("/api/history/clear", "DELETE", null, token);
}
