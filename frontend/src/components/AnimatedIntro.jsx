import React, { useState } from "react";
import useTypewriter from "../hooks/useTypewriter";

export default function AnimatedIntro() {
  const introText =
    "Em um mundo cada vez mais polarizado, nosso objetivo é detectar notícias falsas de forma imparcial. Vamos analisar sua dúvida agora.";
  const highlightText = "detectar notícias falsas de forma imparcial";

  const [done, setDone] = useState(false);

  const typed = useTypewriter(introText, {
    speed: 60,
    highlight: highlightText,
    onDone: () => setDone(true),
  });

  return (
    <div className="w-full flex flex-col items-center">
      {/* Texto animado */}
      <div
        className="animated-intro text-center max-w-3xl"
        dangerouslySetInnerHTML={{ __html: typed }}
      />

      {/* Fade overlay opcional — sem bloquear cliques */}
      {!done && (
        <div
          className="
            pointer-events-none 
            absolute inset-0 
            bg-gradient-to-b from-white/80 to-white/0 
            transition-opacity
          "
        />
      )}
    </div>
  );
}
