import React, { useEffect, useState } from "react";
import { getHistory, getHistoryItem, deleteHistoryItem } from "../api/api.jsx";

export default function HistoryPanel() {
  const [list, setList] = useState([]);
  const [loading, setLoading] = useState(true);
  const [expandedItems, setExpandedItems] = useState(new Set());
  const [itemDetails, setItemDetails] = useState({});

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

  async function toggleItemDetails(id) {
    if (expandedItems.has(id)) {
      // Fechar
      setExpandedItems((prev) => {
        const next = new Set(prev);
        next.delete(id);
        return next;
      });
    } else {
      // Abrir e buscar detalhes se não tiver
      setExpandedItems((prev) => new Set(prev).add(id));
      
      if (!itemDetails[id]) {
        try {
          const details = await getHistoryItem(id);
          setItemDetails((prev) => ({ ...prev, [id]: details }));
        } catch (err) {
          console.error("Erro ao buscar detalhes do item:", err);
        }
      }
    }
  }

  async function handleDelete(id) {
    if (!confirm("Excluir este item do histórico?")) return;

    try {
      await deleteHistoryItem(id);
      // Atualiza lista local
      setList((prev) => prev.filter((item) => item.id !== id));
      // Remove dos detalhes e expandidos
      setItemDetails((prev) => {
        const next = { ...prev };
        delete next[id];
        return next;
      });
      setExpandedItems((prev) => {
        const next = new Set(prev);
        next.delete(id);
        return next;
      });
    } catch (err) {
      console.error("Erro ao deletar item:", err);
    }
  }

  function formatResult(result) {
    if (!result) return null;
    
    if (typeof result === "string") {
      try {
        result = JSON.parse(result);
      } catch {
        return result;
      }
    }
    
    if (typeof result === "object" && result.score !== undefined) {
      return result;
    }
    
    return result;
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
          className="px-3 py-1 rounded bg-blue-600 text-white text-sm hover:bg-blue-700"
        >
          Atualizar
        </button>
      </div>
      <div className="flex flex-col gap-2">
        {list.map((item) => {
          const isExpanded = expandedItems.has(item.id);
          const details = itemDetails[item.id];
          const result = details ? formatResult(details.result) : null;
          
          return (
            <div
              key={item.id}
              className="flex flex-col gap-2 p-3 bg-white border border-gray-200 rounded-lg"
            >
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1">
                  <div className="font-semibold">{item.text_preview}</div>
                  <div className="text-sm text-gray-500 mt-1">
                    {item.date ? new Date(item.date).toLocaleDateString("pt-BR") : "Data não disponível"}
                  </div>
                  <div className="text-sm mt-1">
                    <span className={`
                      px-2 py-1 rounded text-xs font-medium
                      ${item.status === "COMPLETED" 
                        ? "bg-green-100 text-green-800" 
                        : item.status === "ERROR"
                        ? "bg-red-100 text-red-800"
                        : "bg-yellow-100 text-yellow-800"}
                    `}>
                      {item.status}
                    </span>
                  </div>
                </div>
                <div className="flex flex-col gap-2">
                  <button
                    onClick={() => toggleItemDetails(item.id)}
                    className="px-3 py-1 rounded bg-blue-600 text-white text-sm hover:bg-blue-700"
                  >
                    {isExpanded ? "Ocultar" : "Ver detalhes"}
                  </button>
                  <button
                    onClick={() => handleDelete(item.id)}
                    className="px-3 py-1 rounded bg-red-600 text-white text-sm hover:bg-red-700"
                  >
                    Excluir
                  </button>
                </div>
              </div>
              
              {isExpanded && result && (
                <div className="mt-3 pt-3 border-t border-gray-200">
                  {typeof result === "object" && result.score !== undefined ? (
                    <div className="space-y-2">
                      <div className="flex items-center gap-2">
                        <span className="font-medium">Veredito:</span>
                        <span className={`
                          px-3 py-1 rounded-full text-sm font-bold
                          ${result.veredito === "VERDADEIRA" 
                            ? "bg-green-500 text-white" 
                            : result.veredito === "FALSA"
                            ? "bg-red-500 text-white"
                            : "bg-yellow-500 text-white"}
                        `}>
                          {result.veredito}
                        </span>
                      </div>
                      
                      <div className="flex items-center gap-2">
                        <span className="font-medium">Score:</span>
                        <div className="flex-1 bg-gray-200 rounded-full h-4 overflow-hidden">
                          <div 
                            className={`
                              h-full transition-all duration-500
                              ${result.score >= 70 
                                ? "bg-green-500" 
                                : result.score >= 40
                                ? "bg-yellow-500"
                                : "bg-red-500"}
                            `}
                            style={{ width: `${result.score}%` }}
                          />
                        </div>
                        <span className="text-sm font-medium">{result.score}/100</span>
                      </div>
                      
                      {result.explicacao && (
                        <div>
                          <span className="font-medium">Explicação:</span>
                          <div className="mt-1 text-sm text-gray-700">{result.explicacao}</div>
                        </div>
                      )}
                      
                      {result.fontes && result.fontes.length > 0 && (
                        <div>
                          <span className="font-medium">Fontes:</span>
                          <ul className="mt-1 list-disc list-inside text-sm text-gray-700">
                            {result.fontes.map((fonte, idx) => (
                              <li key={idx}>
                                <a 
                                  href={fonte} 
                                  target="_blank" 
                                  rel="noopener noreferrer"
                                  className="text-blue-600 hover:underline"
                                >
                                  {fonte}
                                </a>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  ) : (
                    <div className="text-sm text-gray-700">
                      {typeof result === "string" ? result : JSON.stringify(result, null, 2)}
                    </div>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
