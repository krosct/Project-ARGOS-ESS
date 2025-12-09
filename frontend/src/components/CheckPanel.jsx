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

  React.useEffect(() => setCount(text.length), [text]);

  async function handleCheck() {
    if (!text.trim() || loading) return;

    setLoading(true);
    setResult("Enviando para checagem...");

    try {
      const check = await submitCheck(text);

      if (!check || !check.id) throw new Error("Resposta inválida do servidor");

      let status = check;
      const maxAttempts = 30;
      let attempts = 0;

      while (status.status !== "COMPLETED" && attempts < maxAttempts) {
        await new Promise((resolve) => setTimeout(resolve, 1000));
        status = await getCheckStatus(check.id);
        attempts++;
      }

      if (status.status !== "COMPLETED") {
        setResult("A checagem demorou muito. Tente novamente mais tarde.");
      } else {
        setResult(status.result || status.status);
        add(text, status.result || status.status);
      }

      setText("");
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
        className="
          w-full p-3 rounded-xl border border-gray-300 
          bg-white resize-none h-28 
          focus:outline-none focus:ring-2 focus:ring-blue-500
        "
      />

      <div className="flex items-center justify-between mt-2">
        <div className="text-sm text-gray-600">{count} / 150</div>

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
        <div className="bg-white p-3 rounded-lg border border-gray-200 mt-2 w-full">
          <strong>Resultado:</strong>
          <div className="mt-2 text-sm text-gray-800">{result}</div>
        </div>
      )}

      <FeedbackPanel />
    </div>
  );
}
