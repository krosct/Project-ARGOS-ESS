import React, { useEffect, useState } from 'react'
import { useHistory } from '../hooks/useHistory'
import FeedbackPanel from './FeedbackPanel'

function simpleCheck(text){
  if(!text.trim()) return 'Texto vazio — insira algo para checar.';
  const lower = text.toLowerCase();
  const suspiciousWords = ['clique aqui','compartilhe','segredo','garantia','viral','comprova','exclusivo'];
  const contains = suspiciousWords.filter(w=>lower.includes(w));
  if(contains.length>0) return `Possível conteúdo sensacionalista / enganoso (palavras: ${contains.join(', ')}).`;
  if(lower.length < 30) return 'Texto curto — pode faltar contexto. Verifique fontes e autoria.';
  return 'Nenhum sinal claro de manipulação pelo heurístico simples. Recomendamos checar fontes e data.';
}

export default function CheckPanel(){
  const { add } = useHistory();
  const [text, setText] = useState('');
  const [result, setResult] = useState(null);

  const [count, setCount] = useState(0);

  useEffect(()=> setCount(text.length), [text]);

  function handleCheck(){
    const res = simpleCheck(text);
    setResult(res);
    add(text, res);
    setText('');
  }

  return (
    <div className="flex flex-col gap-4">
      <div className="text-xl font-bold">Vamos começar a checagem</div>

      <textarea
        value={text}
        onChange={(e)=>setText(e.target.value)}
        maxLength={150}
        placeholder="Cole o texto aqui (máx 150 caracteres)"
        className="w-full p-3 rounded-xl border border-gray-300 bg-white resize-none h-28"
      />

      <div className="flex items-center justify-between">
        <div className="text-sm text-gray-600">{count} / 150</div>
        <button onClick={handleCheck} disabled={!text.trim()} className="btn bg-accent hover:opacity-90 text-white px-4 py-2 rounded-xl disabled:opacity-60">
          Checar
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
  )
}
