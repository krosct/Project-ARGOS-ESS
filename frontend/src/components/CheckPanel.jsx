import React, { useState } from "react";
import { useHistory } from "../hooks/useHistory";
import FeedbackPanel from "./FeedbackPanel";
import { submitCheck, getCheckStatus } from "../api/api.jsx";

function isUrl(text) {
  try {
    const url = new URL(text.trim());
    return url.protocol === "http:" || url.protocol === "https:";
  } catch {
    return false;
  }
}

export default function CheckPanel() {
  const { add, fetchHistory } = useHistory();
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [count, setCount] = useState(0);
  const [loading, setLoading] = useState(false);
  const [isUrlInput, setIsUrlInput] = useState(false);

  React.useEffect(() => {
    setCount(text.length);
    setIsUrlInput(isUrl(text));
  }, [text]);

  async function handleCheck() {
    if (!text.trim() || loading) return;

    // Validação básica
    if (!isUrlInput && text.trim().length < 10) {
      setResult("Por favor, insira pelo menos 10 caracteres de texto.");
      return;
    }

    setLoading(true);
    setResult(null);

    try {
      const check = await submitCheck(text.trim());

      if (!check || !check.id) throw new Error("Resposta inválida do servidor");

      // Polling para verificar status
      let status = check;
      const maxAttempts = 60; // Aumentado para 60 segundos
      let attempts = 0;

      while (status.status !== "COMPLETED" && status.status !== "FAILED" && attempts < maxAttempts) {
        await new Promise((resolve) => setTimeout(resolve, 1000));
        status = await getCheckStatus(check.id);
        attempts++;
      }

      if (status.status === "FAILED") {
        setResult(`Erro: ${status.result || "Falha ao processar a checagem."}`);
      } else if (status.status !== "COMPLETED") {
        setResult("A checagem está demorando mais que o esperado. Você pode verificar o status mais tarde no histórico.");
      } else {
        setResult(status.result || "Análise concluída.");
        add(text.trim(), status.result || status.status);
        fetchHistory(); // Atualiza o histórico
      }

      setText("");
    } catch (err) {
      console.error("Erro ao checar:", err);
      setResult(`Erro ao checar no servidor: ${err.message || "Tente novamente."}`);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex flex-col gap-4 w-full">
      <div className="text-xl font-bold">Vamos começar a checagem</div>

      <div className="flex flex-col gap-2">
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          maxLength={isUrlInput ? 5000 : 5000}
          placeholder={
            isUrlInput
              ? "Cole a URL aqui (ex: https://exemplo.com/noticia)"
              : "Cole o texto ou URL aqui (mín. 10 caracteres para texto)"
          }
          className="
            w-full p-3 rounded-xl border border-gray-300 
            bg-white resize-none h-32
            focus:outline-none focus:ring-2 focus:ring-blue-500
          "
        />

        {isUrlInput && (
          <div className="text-sm text-blue-600 flex items-center gap-1">
            <span>🔗</span>
            <span>URL detectada - o conteúdo será extraído automaticamente</span>
          </div>
        )}
      </div>

      <div className="flex items-center justify-between mt-2">
        <div className="text-sm text-gray-600">
          {count} / {isUrlInput ? "5000" : "5000"} caracteres
        </div>

        <button
          onClick={handleCheck}
          disabled={!text.trim() || loading}
          className={`
            px-6 py-2 
            rounded-full
            bg-blue-600 
            hover:bg-blue-700
            text-white 
            font-medium
            flex items-center gap-2
            shadow-sm
            transition-all duration-200
            disabled:opacity-50 disabled:cursor-not-allowed
            hover:shadow-md
            ${!loading ? "hover:scale-[1.03]" : ""}
          `}
        >
          {loading && (
            <span className="animate-spin w-4 h-4 border-2 border-white border-t-transparent rounded-full" />
          )}

          {loading ? "Checando..." : "Checar"}
        </button>
      </div>

      {result && (
        <div className="bg-white p-4 rounded-lg border border-gray-200 mt-2 w-full shadow-sm">
          <strong className="text-gray-800">Resultado:</strong>
          <div className="mt-2 text-sm text-gray-800 whitespace-pre-wrap">{result}</div>
        </div>
      )}

      <FeedbackPanel />
    </div>
  );
}
