import React, { useState } from 'react'

export default function FeedbackPanel(){
  const [text, setText] = useState('');
  const [sent, setSent] = useState(false);

  function send(){
    if(!text.trim()) return alert('Por favor, escreva um comentário antes de enviar.');
    setText('');
    setSent(true);
    setTimeout(()=>setSent(false), 3000);
  }

  return (
    <div className="mt-4 bg-gray-50 p-4 rounded-xl border border-gray-100">
      <p className="text-sm">Deixe um comentário se você gostou ou não da resposta — nos ajude a melhorar.</p>
      <textarea value={text} onChange={e=>setText(e.target.value)} placeholder="Escreva seu comentário aqui..." className="w-full h-20 mt-2 p-2 rounded-lg border border-gray-300 resize-none" />
      <div className="flex items-center justify-end gap-2 mt-2">
        <button onClick={send} className="btn bg-accent text-white px-4 py-2 rounded-xl">Enviar</button>
      </div>
      {sent && <div className="text-sm text-green-600 mt-2">Obrigado pelo seu comentário!</div>}
    </div>
  )
}
