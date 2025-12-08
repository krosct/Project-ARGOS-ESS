import React, { createContext, useContext, useEffect, useState } from "react";

const STORAGE_KEY = "argos_history_v1";
const HistoryContext = createContext(null);

export function HistoryProvider({ children }) {
  const [list, setList] = useState([]);

  // Carrega do localStorage
  useEffect(() => {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      setList(raw ? JSON.parse(raw) : []);
    } catch (e) {
      setList([]);
    }
  }, []);

  // Salva sempre que a lista muda
  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(list));
    } catch (e) {}
  }, [list]);

  // Adiciona item ao histórico
  function add({ id, text, result, created_at }) {
    const item = {
      id: id ?? Date.now(),
      text,
      result,
      created_at: created_at ?? new Date().toISOString(),
    };

    const next = [item, ...list];
    if (next.length > 200) next.length = 200; // Limite opcional

    setList(next);
  }

  // Remove item
  function remove(id) {
    setList(list.filter((item) => item.id !== id));
  }

  return (
    <HistoryContext.Provider value={{ list, add, remove }}>
      {children}
    </HistoryContext.Provider>
  );
}

export function useHistory() {
  const ctx = useContext(HistoryContext);
  if (!ctx) throw new Error("useHistory must be used inside HistoryProvider");
  return ctx;
}
