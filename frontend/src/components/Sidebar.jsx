import React from 'react'

export default function Sidebar({view, setView}){
  return (
    <aside className="w-64 bg-gray-100 p-5 border-r border-gray-200 hidden md:flex flex-col gap-4">
      <img src="/argos.png" alt="Argos" className="mx-auto rounded-lg max-w-[120px]" />
      <div className="text-center font-bold text-lg">Argos — Checagem</div>

      <nav className="flex flex-col gap-2 mt-2">
        <button onClick={()=>setView('new')} className={`flex items-center gap-3 px-3 py-2 rounded-lg font-semibold text-left ${view==='new' ? 'bg-gray-200' : 'hover:bg-gray-200'}`}>
          <i className="fa-solid fa-magnifying-glass"></i>
          Nova checagem
        </button>

        <button onClick={()=>setView('history')} className={`flex items-center gap-3 px-3 py-2 rounded-lg font-semibold text-left ${view==='history' ? 'bg-gray-200' : 'hover:bg-gray-200'}`}>
          <i className="fa-solid fa-list"></i>
          Histórico
        </button>
      </nav>

      <div className="mt-auto text-sm text-gray-500">Histórico salvo localmente no navegador</div>
    </aside>
  )
}
