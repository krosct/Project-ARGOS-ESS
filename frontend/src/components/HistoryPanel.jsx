import React from 'react'
import { useHistory } from '../hooks/useHistory'

export default function HistoryPanel(){
  const { list, remove } = useHistory();

  if(!list.length) return <div className="text-gray-500">Nenhuma checagem salva ainda.</div>

  return (
    <div className="flex flex-col gap-3">
      <div className="text-xl font-bold">Histórico de checagens</div>
      <div className="flex flex-col gap-2">
        {list.map(item=> (
          <div key={item.id} className="flex items-start justify-between gap-4 p-3 bg-white border border-gray-200 rounded-lg">
            <div className="flex-1">
              <div className="font-semibold">{item.text.length>80 ? item.text.slice(0,77)+'…' : item.text}</div>
              <div className="text-sm text-gray-500 mt-1">{new Date(item.at).toLocaleString()}</div>
              <div className="text-sm text-gray-700 mt-2">{item.result}</div>
            </div>
            <div className="flex flex-col gap-2">
              <button onClick={()=>{ if(confirm('Excluir este item do histórico?')) remove(item.id) }} className="px-3 py-1 rounded bg-red-600 text-white text-sm">Excluir</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
