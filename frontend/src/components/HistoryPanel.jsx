import React, { useEffect, useState } from "react";
import { getHistory, deleteHistoryItem } from "../api/api.jsx";

export default function HistoryPanel() {
  const [list, setList] = useState([]);
  const [loading, setLoading] = useState(true);

  // Carrega histórico ao montar o componente
  useEffect(() => {
    fetchHistory();
  }, []);

  async function fetchHistory() {
    try {
      setLoading(true);
      const data = await getHistory();
      setList(data || []);
    } catch (err) {
      console.error("Erro ao carregar histórico:", err);
      setList([]);
    } finally {
      setLoading(false);
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
      alert("Erro ao deletar item. Tente novamente.");
    }
  }

  if (loading) {
    return <div className="text-gray-500">Carregando histórico...</div>;
  }

  if (!list.length) {
    return <div className="text-gray-500">Nenhuma checagem salva ainda.</div>;
  }

  return (
    <div className="flex flex-col gap-3">
      <div className="flex items-center justify-between">
        <div className="text-xl font-bold">Histórico de checagens</div>
        <button
          onClick={fetchHistory}
          className="text-sm text-blue-600 hover:text-blue-700 px-2 py-1"
        >
          Atualizar
        </button>
      </div>
      <div className="flex flex-col gap-2">
        {list.map((item) => (
          <div
            key={item.id}
            className="flex items-start justify-between gap-4 p-4 bg-white border border-gray-200 rounded-lg shadow-sm hover:shadow-md transition-shadow"
          >
            <div className="flex-1 min-w-0">
              <div className="font-semibold text-gray-800 break-words">
                {item.text && item.text.length > 100
                  ? item.text.slice(0, 97) + "…"
                  : item.text || item.text_preview || "Sem texto"}
              </div>
              <div className="text-sm text-gray-500 mt-1">
                {item.created_at
                  ? new Date(item.created_at).toLocaleString("pt-BR")
                  : item.date || "Data não disponível"}
              </div>
              {item.status && (
                <div className="text-xs mt-1">
                  <span
                    className={`px-2 py-1 rounded ${
                      item.status === "COMPLETED"
                        ? "bg-green-100 text-green-800"
                        : item.status === "ANALYSING"
                        ? "bg-yellow-100 text-yellow-800"
                        : item.status === "FAILED"
                        ? "bg-red-100 text-red-800"
                        : "bg-gray-100 text-gray-800"
                    }`}
                  >
                    {item.status}
                  </span>
                </div>
              )}
              {item.result && (
                <div className="text-sm text-gray-700 mt-3 p-2 bg-gray-50 rounded whitespace-pre-wrap break-words">
                  {item.result}
                </div>
              )}
            </div>
            <div className="flex flex-col gap-2">
              <button
                onClick={() => handleDelete(item.id)}
                className="px-3 py-1 rounded bg-red-600 text-white text-sm hover:bg-red-700 transition-colors"
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
