import React, { useState, useEffect } from "react";

export default function AnimatedIntro() {
  const introText =
    "Em um mundo cada vez mais polarizado, nosso objetivo é detectar notícias falsas de forma imparcial. Vamos analisar sua dúvida agora.";
  const highlightText = "detectar notícias falsas de forma imparcial";

  const [typed, setTyped] = useState("");
  const [done, setDone] = useState(false);

  // Variável para controlar a velocidade (ms por letra)
  const typingSpeed = 80; // altere aqui para mais rápido ou mais lento

  useEffect(() => {
    setTyped("");
    setDone(false);
    let i = 0;

    const interval = setInterval(() => {
      setTyped(introText.slice(0, i + 1));
      i++;

      if (i >= introText.length) {
        clearInterval(interval);
        setDone(true);
      }
    }, typingSpeed); // usa a variável

    return () => clearInterval(interval);
  }, [typingSpeed]); // adiciona a dependência

  // Renderiza o texto com destaque laranja
  const renderText = () => {
    const index = typed.indexOf(highlightText);
    if (index === -1) return typed;

    const before = typed.slice(0, index);
    const after = typed.slice(index + highlightText.length);

    return (
      <>
        {before}
        <span style={{ color: "orange", fontWeight: "bold" }}>
          {highlightText}
        </span>
        {after}
      </>
    );
  };

  return (
    <div className="w-full flex flex-col items-center mb-14 text-center max-w-3xl">
      <div className="text-3xl md:text-5xl font-semibold leading-snug text-gray-900">
        {renderText()}
        {!done && (
          <span className="inline-block w-1 bg-gray-900 animate-pulse ml-1">
            &nbsp;
          </span>
        )}
      </div>
    </div>
  );
}
