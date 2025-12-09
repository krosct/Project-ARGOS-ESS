import React, { useEffect, useState } from "react";
import { getHistory, deleteHistoryItem } from "../api/api.jsx";

export default function HistoryPanel() {
  const [list, setList] = useState([]);

  // Carrega histórico ao montar o componente
  useEffect(() => {
    fetchHistory();
  }, []);

  async function fetchHistory() {
    try {
      const data = await getHistory();
      setList(data);
    } catch (err) {
      console.error("Erro ao carregar histórico:", err);
    }
  }

  async function handleDelete(id) {
    if (!confirm("Excluir este item do histórico?")) return;

    try {
      await deleteHistoryItem(id);
      // Atualiza lista local
      setList((prev) => prev.filter((item) => item.id !== id));
    } catch (err) {
      console.error("Erro ao deletar item:", err);
    }
  }

  if (!list.length)
    return <div className="text-gray-500">Nenhuma checagem salva ainda.</div>;

  return (
    <div className="flex flex-col gap-3">
      <div className="text-xl font-bold">Histórico de checagens</div>
      <div className="flex flex-col gap-2">
        {list.map((item) => (
          <div
            key={item.id}
            className="flex items-start justify-between gap-4 p-3 bg-white border border-gray-200 rounded-lg"
          >
            <div className="flex-1">
              <div className="font-semibold">
                {item.text.length > 80
                  ? item.text.slice(0, 77) + "…"
                  : item.text}
              </div>
              <div className="text-sm text-gray-500 mt-1">
                {new Date(item.created_at).toLocaleString()}
              </div>
              <div className="text-sm text-gray-700 mt-2">{item.result}</div>
            </div>
            <div className="flex flex-col gap-2">
              <button
                onClick={() => handleDelete(item.id)}
                className="px-3 py-1 rounded bg-red-600 text-white text-sm"
              >
                Excluir
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
