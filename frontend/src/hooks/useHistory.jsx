import React, { createContext, useContext, useEffect, useState } from "react";
import { getHistory, getHistoryItem, deleteHistoryItem } from "../api/api.jsx";

const HistoryContext = createContext(null);

export function HistoryProvider({ children }) {
  const [list, setList] = useState([]);
  const [loading, setLoading] = useState(true);

  // Carrega histórico do backend ao montar
  useEffect(() => {
    fetchHistory();
  }, []);

  async function fetchHistory() {
    try {
      setLoading(true);
      const data = await getHistory();
      setList(data);
    } catch (err) {
      console.error("Erro ao carregar histórico:", err);
      setList([]);
    } finally {
      setLoading(false);
    }
  }

  // Adiciona novo item no histórico
  // Mantemos assinatura original, mas agora pode ser chamado após criar check via backend
  function add(text, result) {
    const next = [
      {
        id: Date.now().toString(),
        text,
        result,
        created_at: new Date().toISOString(),
      },
      ...list,
    ];
    if (next.length > 200) next.length = 200;
    setList(next);
  }

  // Remove item do backend e atualiza localmente
  async function remove(id) {
    try {
      await deleteHistoryItem(id);
      setList((prev) => prev.filter((i) => i.id !== id));
    } catch (err) {
      console.error("Erro ao deletar item do histórico:", err);
      // fallback local
      setList((prev) => prev.filter((i) => i.id !== id));
    }
  }

  return (
    <HistoryContext.Provider
      value={{ list, add, remove, loading, fetchHistory }}
    >
      {children}
    </HistoryContext.Provider>
  );
}

export function useHistory() {
  const ctx = useContext(HistoryContext);
  if (!ctx) throw new Error("useHistory must be used inside HistoryProvider");
  return ctx;
}
