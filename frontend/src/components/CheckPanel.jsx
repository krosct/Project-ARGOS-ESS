import React, { useEffect, useState } from "react";
import { useHistory } from "../hooks/useHistory";
import FeedbackPanel from "./FeedbackPanel";
import { submitCheck, getCheckStatus } from "../api/api.jsx";

export default function CheckPanel() {
  const { add } = useHistory();
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [count, setCount] = useState(0);
  const [loading, setLoading] = useState(false);

  useEffect(() => setCount(text.length), [text]);

  async function handleCheck() {
    if (!text.trim()) return;

    setLoading(true);
    setResult("Enviando para checagem...");
    try {
      // Envia o texto para criar a checagem
      const check = await submitCheck(text);

      // Polling: verifica status a cada 1s até COMPLETED
      let status = check;
      while (status.status !== "COMPLETED") {
        await new Promise((resolve) => setTimeout(resolve, 1000));
        status = await getCheckStatus(check.id);
      }

      setResult(status.result || status.status);
      add(text, status.result || status.status);
      setText("");
    } catch (err) {
      console.error(err);
      setResult("Erro ao checar no servidor. Tente novamente.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex flex-col gap-4">
      <div className="text-xl font-bold">Vamos começar a checagem</div>

      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        maxLength={150}
        placeholder="Cole o texto aqui (máx 150 caracteres)"
        className="w-full p-3 rounded-xl border border-gray-300 bg-white resize-none h-28"
      />

      <div className="flex items-center justify-between">
        <div className="text-sm text-gray-600">{count} / 150</div>
        <button
          onClick={handleCheck}
          disabled={!text.trim() || loading}
          className="btn bg-accent hover:opacity-90 text-white px-4 py-2 rounded-xl disabled:opacity-60"
        >
          {loading ? "Checando..." : "Checar"}
        </button>
      </div>

      {result && (
        <div className="bg-white p-3 rounded-lg border border-gray-200">
          <strong>Resultado:</strong>
          <div className="mt-2 text-sm text-gray-800">{result}</div>
        </div>
      )}

      <FeedbackPanel />
    </div>
  );
}
