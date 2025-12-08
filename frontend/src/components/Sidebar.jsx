import React from "react";
import { Search, History } from "lucide-react";

export default function Sidebar({ view, setView }) {
  return (
    <aside className="w-64 bg-gray-50 p-6 border-r border-gray-200 hidden md:flex flex-col gap-6">
      {/* Logo */}
      <div className="flex flex-col items-center gap-3">
        <img
          src="/argos.png"
          alt="Argos"
          className="mx-auto rounded-lg w-24 h-24 object-cover shadow-sm"
        />
        <h1 className="text-xl font-bold text-gray-800">Argos — Checagem</h1>
      </div>

      {/* Botões */}
      <nav className="flex flex-col gap-3">
        {/* Nova checagem */}
        <button
          onClick={() => setView("new")}
          role="button"
          aria-selected={view === "new"}
          className={`flex items-center gap-3 px-4 py-2 rounded-lg font-medium transition-all 
            ${
              view === "new"
                ? "bg-gray-200 border-l-4 border-blue-500"
                : "hover:bg-gray-100 border-l-4 border-transparent"
            }`}
        >
          <Search size={20} />
          Nova checagem
        </button>

        {/* Histórico */}
        <button
          onClick={() => setView("history")}
          role="button"
          aria-selected={view === "history"}
          className={`flex items-center gap-3 px-4 py-2 rounded-lg font-medium transition-all 
            ${
              view === "history"
                ? "bg-gray-200 border-l-4 border-blue-500"
                : "hover:bg-gray-100 border-l-4 border-transparent"
            }`}
        >
          <History size={20} />
          Histórico
        </button>
      </nav>

      {/* Rodapé */}
      <div className="mt-auto text-sm text-gray-500">
        Histórico salvo localmente no navegador
      </div>
    </aside>
  );
}
