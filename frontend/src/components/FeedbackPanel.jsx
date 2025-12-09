import React, { useState } from "react";

export default function FeedbackPanel() {
  const [text, setText] = useState("");
  const [sent, setSent] = useState(false);

  function send() {
    if (!text.trim()) return; // botão já desabilitado quando vazio
    setText("");
    setSent(true);
    setTimeout(() => setSent(false), 3000);
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
        className="w-full h-24 mt-2 p-3 rounded-lg border border-gray-300 resize-none focus:outline-none focus:ring-2 focus:ring-blue-400"
      />

      <div className="flex items-center justify-end mt-2">
        <button
          onClick={send}
          disabled={!text.trim()}
          className="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-xl disabled:opacity-50 transition-colors duration-200"
        >
          Enviar
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
