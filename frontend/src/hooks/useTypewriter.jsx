import { useState, useEffect } from "react";

export default function useTypewriter(text, { speed = 60, onDone } = {}) {
  const [typed, setTyped] = useState("");

  useEffect(() => {
    if (!text) return;
    setTyped("");
    let i = 0;

    const interval = setInterval(() => {
      setTyped((prev) => prev + text[i]);
      i++;

      if (i >= text.length) {
        clearInterval(interval);
        if (onDone) onDone();
      }
    }, speed);

    return () => clearInterval(interval);
  }, [text, speed, onDone]);

  return typed;
}
