import React, { useState } from "react";
import { useHistory } from "../hooks/useHistory";
import FeedbackPanel from "./FeedbackPanel";
import { submitCheck, getCheckStatus } from "../api/api.jsx";

export default function CheckPanel() {
  const { add } = useHistory();
  const [inputType, setInputType] = useState("text"); // "text" ou "url"
  const [text, setText] = useState("");
  const [url, setUrl] = useState("");
  const [result, setResult] = useState(null);
  const [count, setCount] = useState(0);
  const [loading, setLoading] = useState(false);

  React.useEffect(() => {
    if (inputType === "text") {
      setCount(text.length);
    } else {
      setCount(url.length);
    }
  }, [text, url, inputType]);

  async function handleCheck() {
    const hasText = text.trim();
    const hasUrl = url.trim();
    
    if ((!hasText && !hasUrl) || loading) return;

    setLoading(true);
    setResult({ type: "loading", message: "Enviando para checagem..." });

    try {
      const requestData = {};
      if (inputType === "text" && hasText) {
        requestData.text = text.trim();
      } else if (inputType === "url" && hasUrl) {
        requestData.url = url.trim();
      }

      const check = await submitCheck(requestData);

      if (!check || !check.id) throw new Error("Resposta inválida do servidor");

      // O backend já retorna o resultado completo se estiver COMPLETED
      if (check.status === "COMPLETED" && check.result) {
        setResult({ type: "success", data: check.result });
        const inputValue = inputType === "text" ? text : url;
        await add(inputValue, check.result);
        if (inputType === "text") setText("");
        else setUrl("");
      } else {
        // Se ainda estiver processando, fazer polling
        let status = check;
        const maxAttempts = 30;
        let attempts = 0;

        while (status.status !== "COMPLETED" && status.status !== "ERROR" && attempts < maxAttempts) {
          await new Promise((resolve) => setTimeout(resolve, 1000));
          status = await getCheckStatus(check.id);
          attempts++;
        }

        if (status.status === "COMPLETED" && status.result) {
          // Parse do resultado se vier como string JSON
          let resultData = status.result;
          if (typeof resultData === "string") {
            try {
              resultData = JSON.parse(resultData);
            } catch (e) {
              console.error("Erro ao fazer parse do resultado:", e);
            }
          }
          
          // Se resultData for um objeto NewsAnalysisResult
          if (resultData && typeof resultData === "object" && "score" in resultData) {
            setResult({ type: "success", data: resultData });
            const inputValue = inputType === "text" ? text : url;
            await add(inputValue, resultData);
          } else {
            setResult({ type: "error", message: "Resultado em formato inesperado" });
          }
        } else if (status.status === "ERROR") {
          let errorMsg = "Erro ao processar a checagem";
          if (status.result) {
            try {
              const errorData = typeof status.result === "string" ? JSON.parse(status.result) : status.result;
              errorMsg = errorData.error || errorMsg;
            } catch (e) {
              // Ignora erro de parse
            }
          }
          setResult({ type: "error", message: errorMsg });
        } else {
          setResult({ type: "error", message: "A checagem demorou muito. Tente novamente mais tarde." });
        }

        if (inputType === "text") setText("");
        else setUrl("");
      }
    } catch (err) {
      console.error("Erro ao checar:", err);
      setResult({ 
        type: "error", 
        message: err.message || "Erro ao checar no servidor. Tente novamente." 
      });
    } finally {
      setLoading(false);
    }
  }

  const canSubmit = inputType === "text" ? text.trim() : url.trim();

  return (
    <div className="flex flex-col gap-4 w-full">
      <div className="text-xl font-bold">Vamos começar a checagem</div>

      {/* Seletor de tipo de entrada */}
      <div className="flex gap-2">
        <button
          onClick={() => {
            setInputType("text");
            setResult(null);
          }}
          className={`
            px-4 py-2 rounded-lg font-medium transition-all
            ${inputType === "text" 
              ? "bg-blue-600 text-white" 
              : "bg-gray-200 text-gray-700 hover:bg-gray-300"}
          `}
        >
          Texto
        </button>
        <button
          onClick={() => {
            setInputType("url");
            setResult(null);
          }}
          className={`
            px-4 py-2 rounded-lg font-medium transition-all
            ${inputType === "url" 
              ? "bg-blue-600 text-white" 
              : "bg-gray-200 text-gray-700 hover:bg-gray-300"}
          `}
        >
          URL
        </button>
      </div>

      {/* Campo de entrada baseado no tipo */}
      {inputType === "text" ? (
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
      ) : (
        <input
          type="url"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Cole a URL da notícia aqui (ex: https://exemplo.com/noticia)"
          className="
            w-full p-3 rounded-xl border border-gray-300 
            bg-white
            focus:outline-none focus:ring-2 focus:ring-blue-500
          "
        />
      )}

      <div className="flex items-center justify-between mt-2">
        <div className="text-sm text-gray-600">
          {inputType === "text" ? `${count} / 150` : `${count} caracteres`}
        </div>

        <button
          onClick={handleCheck}
          disabled={!canSubmit || loading}
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

      {/* Exibição do resultado */}
      {result && (
        <div className={`
          p-4 rounded-lg border mt-2 w-full
          ${result.type === "error" 
            ? "bg-red-50 border-red-200" 
            : result.type === "loading"
            ? "bg-blue-50 border-blue-200"
            : "bg-green-50 border-green-200"}
        `}>
          {result.type === "loading" && (
            <div className="text-sm text-blue-800">{result.message}</div>
          )}
          
          {result.type === "error" && (
            <div>
              <strong className="text-red-800">Erro:</strong>
              <div className="mt-2 text-sm text-red-700">{result.message}</div>
            </div>
          )}
          
          {result.type === "success" && result.data && (
            <div>
              <strong className="text-green-800">Resultado da Análise:</strong>
              <div className="mt-3 space-y-2">
                <div className="flex items-center gap-2">
                  <span className="font-medium">Veredito:</span>
                  <span className={`
                    px-3 py-1 rounded-full text-sm font-bold
                    ${result.data.veredito === "VERDADEIRA" 
                      ? "bg-green-500 text-white" 
                      : result.data.veredito === "FALSA"
                      ? "bg-red-500 text-white"
                      : "bg-yellow-500 text-white"}
                  `}>
                    {result.data.veredito}
                  </span>
                </div>
                
                <div className="flex items-center gap-2">
                  <span className="font-medium">Score:</span>
                  <div className="flex-1 bg-gray-200 rounded-full h-4 overflow-hidden">
                    <div 
                      className={`
                        h-full transition-all duration-500
                        ${result.data.score >= 70 
                          ? "bg-green-500" 
                          : result.data.score >= 40
                          ? "bg-yellow-500"
                          : "bg-red-500"}
                      `}
                      style={{ width: `${result.data.score}%` }}
                    />
                  </div>
                  <span className="text-sm font-medium">{result.data.score}/100</span>
                </div>
                
                {result.data.explicacao && (
                  <div>
                    <span className="font-medium">Explicação:</span>
                    <div className="mt-1 text-sm text-gray-700">{result.data.explicacao}</div>
                  </div>
                )}
                
                {result.data.fontes && result.data.fontes.length > 0 && (
                  <div>
                    <span className="font-medium">Fontes:</span>
                    <ul className="mt-1 list-disc list-inside text-sm text-gray-700">
                      {result.data.fontes.map((fonte, idx) => (
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
            </div>
          )}
        </div>
      )}

      <FeedbackPanel />
    </div>
  );
}
