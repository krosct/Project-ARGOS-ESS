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
  // Como o backend já salva automaticamente, apenas recarrega do servidor
  async function add(text, result) {
    // O backend já salvou o item, então apenas recarregamos
    await fetchHistory();
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
