import React, { useState } from "react";

export default function FeedbackPanel() {
  const [text, setText] = useState("");
  const [sent, setSent] = useState(false);
  const [loading, setLoading] = useState(false);

  function send() {
    if (!text.trim() || loading) return;

    setLoading(true);

    setTimeout(() => {
      setLoading(false);
      setSent(true);
      setText("");

      setTimeout(() => setSent(false), 3000);
    }, 1200); // apenas simulação de envio
  }

  return (
    <div className="mt-4 w-full bg-gray-50 p-4 rounded-xl border border-gray-100 shadow-sm">
      <p className="text-sm text-gray-700">
        Deixe um comentário se você gostou ou não da nossa checagem — nos ajude
        a melhorar. Podemos usar seus dados para personalização, inovação,
        pesquisa e outros fins descritos em nossa Política de Privacidade.
      </p>

      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Escreva seu comentário aqui..."
        className="
          w-full h-24 mt-2 p-3 rounded-lg border border-gray-300 
          resize-none 
          focus:outline-none focus:ring-2 focus:ring-blue-400
        "
      />

      <div className="flex items-center justify-end mt-3">
        <button
          onClick={send}
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

          {loading ? "Enviando..." : "Enviar"}
        </button>
      </div>

      {sent && (
        <div className="text-sm text-green-600 mt-2 animate-fade-in">
          Obrigado pelo seu comentário!
        </div>
      )}
    </div>
  );
}
