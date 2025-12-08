import { useState, useEffect, useRef } from "react";
import { submitCheck, getCheckStatus } from "../api/api";
import { useHistory } from "../hooks/useHistory";

export default function CheckPanel() {
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState(null);
  const [result, setResult] = useState(null);

  const intervalRef = useRef(null);
  const { add } = useHistory();

  // Cleanup: cancelar polling ao desmontar
  useEffect(() => {
    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, []);

  const handleSubmit = async () => {
    try {
      setLoading(true);
      setResult(null);
      setStatus("Enviando...");

      const { id } = await submitCheck(text);
      setStatus("Analisando...");

      let attempts = 0;
      const maxAttempts = 60;

      intervalRef.current = setInterval(async () => {
        attempts++;

        try {
          const response = await getCheckStatus(id);

          if (response.status === "COMPLETED") {
            clearInterval(intervalRef.current);
            setStatus("Concluído");
            setResult(response.result);
            setLoading(false);

            add(text, response.result);
            return;
          }

          if (response.status === "FAILED") {
            clearInterval(intervalRef.current);
            setStatus("Falha ao processar");
            setLoading(false);
            return;
          }
        } catch (err) {
          clearInterval(intervalRef.current);
          setStatus("Erro de comunicação");
          setLoading(false);
          return;
        }

        if (attempts >= maxAttempts) {
          clearInterval(intervalRef.current);
          setStatus("Tempo máximo excedido");
          setLoading(false);
        }
      }, 1000);
    } catch (err) {
      console.error(err);
      setStatus("Erro ao enviar");
      setLoading(false);
    }
  };

  return (
    <div className="p-4 bg-white rounded shadow">
      <h2 className="text-xl font-bold mb-3">Verificar Fake News</h2>

      <textarea
        className="border border-gray-300 p-3 w-full h-32 rounded"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Cole o texto para verificar..."
      />

      <button
        onClick={handleSubmit}
        disabled={loading || !text.trim()}
        className={`mt-4 px-4 py-2 rounded text-white ${
          loading ? "bg-gray-400" : "bg-blue-600 hover:bg-blue-700"
        }`}
      >
        {loading ? "Processando..." : "Verificar"}
      </button>

      {status && (
        <p className="mt-3 text-gray-700">
          <strong>Status:</strong> {status}
        </p>
      )}

      {result && (
        <div className="mt-4 p-4 bg-gray-100 border rounded">
          <h3 className="font-bold">Resultado:</h3>
          <p>{result}</p>
        </div>
      )}
    </div>
  );
}
