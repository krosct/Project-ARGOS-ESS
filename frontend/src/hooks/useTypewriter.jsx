import { useEffect, useState, useRef } from "react";

export default function useTypewriter(
  text,
  { speed = 50, highlight = null, onDone } = {}
) {
  const [output, setOutput] = useState("");
  const [isDone, setIsDone] = useState(false);
  const timeoutRef = useRef(null);
  const indexRef = useRef(0);

  // Função que cancela timeouts
  const clear = () => {
    if (timeoutRef.current) clearTimeout(timeoutRef.current);
  };

  useEffect(() => {
    clear();

    setOutput("");
    setIsDone(false);
    indexRef.current = 0;

    function tick() {
      if (indexRef.current < text.length) {
        const next = text.slice(0, indexRef.current + 1);
        setOutput(next);
        indexRef.current++;

        timeoutRef.current = setTimeout(tick, speed);
      } else {
        setIsDone(true);
        if (typeof onDone === "function") onDone();
      }
    }

    tick();
    return clear;
  }, [text, speed, onDone]); // highlight removido da dependência

  // Highlight seguro: retorna partes para um componente renderizar
  const parts = highlight
    ? output.split(new RegExp(`(${highlight})`, "gi")).map((part) => ({
        text: part,
        highlight: part.toLowerCase() === highlight.toLowerCase(),
      }))
    : [{ text: output, highlight: false }];

  return { output, isDone, parts };
}
