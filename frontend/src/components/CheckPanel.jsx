import React, { useState } from "react";
import { useHistory } from "../hooks/useHistory";
import FeedbackPanel from "./FeedbackPanel";
import { submitCheck, getCheckStatus } from "../api/api.jsx";

export default function CheckPanel() {
  const { add } = useHistory();
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [count, setCount] = useState(0);
  const [loading, setLoading] = useState(false);

  // Atualiza contador de caracteres
  React.useEffect(() => setCount(text.length), [text]);

  async function handleCheck() {
    if (!text.trim() || loading) return; // evita envio vazio ou múltiplo

    setLoading(true);
    setResult("Enviando para checagem...");

    try {
      console.log("Enviando texto para checagem:", text);
      const check = await submitCheck(text);

      if (!check || !check.id) {
        throw new Error("Resposta inválida do servidor");
      }

      console.log("Checagem criada:", check);

      let status = check;
      const maxAttempts = 30; // 30 segundos de polling
      let attempts = 0;

      while (status.status !== "COMPLETED" && attempts < maxAttempts) {
        await new Promise((resolve) => setTimeout(resolve, 1000));
        status = await getCheckStatus(check.id);
        console.log("Status atual:", status.status);
        attempts++;
      }

      if (status.status !== "COMPLETED") {
        setResult("A checagem demorou muito. Tente novamente mais tarde.");
      } else {
        setResult(status.result || status.status);
        add(text, status.result || status.status); // atualiza histórico local
      }

      setText(""); // limpa o textarea após checagem
    } catch (err) {
      console.error("Erro ao checar:", err);
      setResult("Erro ao checar no servidor. Tente novamente.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex flex-col gap-4 w-full">
      <div className="text-xl font-bold">Vamos começar a checagem</div>

      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        maxLength={150}
        placeholder="Cole o texto aqui (máx 150 caracteres)"
        className="w-full p-3 rounded-xl border border-gray-300 bg-white resize-none h-28 focus:outline-none focus:ring-2 focus:ring-blue-400"
      />

      <div className="flex items-center justify-between mt-2">
        <div className="text-sm text-gray-600">{count} / 150</div>
        <button
          onClick={handleCheck}
          disabled={!text.trim() || loading}
          className="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-xl disabled:opacity-50 transition-colors duration-200"
        >
          {loading ? "Checando..." : "Checar"}
        </button>
      </div>

      {result && (
        <div className="bg-white p-3 rounded-lg border border-gray-200 mt-2 w-full">
          <strong>Resultado:</strong>
          <div className="mt-2 text-sm text-gray-800">{result}</div>
        </div>
      )}

      <FeedbackPanel />
    </div>
  );
}
