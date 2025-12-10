import { useEffect, useState, useRef } from "react";

export default function useTypewriter(
  text,
  { speed = 50, highlight = null, onDone } = {}
) {
  const [out, setOut] = useState("");
  const iRef = useRef(0);
  const tRef = useRef(null);

  useEffect(() => {
    iRef.current = 0;
    setOut("");

    function tick() {
      if (iRef.current < text.length) {
        const current = text.slice(0, iRef.current + 1);

        if (highlight && current.includes(highlight)) {
          const safe = current.replace(
            highlight,
            `<span style="color: var(--highlight);">${highlight}</span>`
          );
          setOut(safe);
        } else {
          setOut(current);
        }

        iRef.current++;
        tRef.current = setTimeout(tick, speed);
      } else {
        if (typeof onDone === "function") onDone();
      }
    }

    tick();

    return () => clearTimeout(tRef.current);
  }, [text, speed, highlight, onDone]); // ✅ adicionado onDone

  return out;
}
