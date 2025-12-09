import React, { useEffect, useState } from "react";
import useTypewriter from "../hooks/useTypewriter";

export default function AnimatedIntro() {
  const introText =
    "Em um mundo cada vez mais polarizado, nosso objetivo é detectar notícias falsas de forma imparcial. Vamos analisar sua dúvida agora.";
  const highlightText = "detectar notícias falsas de forma imparcial";
  const [done, setDone] = useState(false);

  const typed = useTypewriter(introText, {
    speed: 50,
    highlight: highlightText,
    onDone: () => setDone(true),
  });

  return (
    <div className="w-full flex flex-col items-center mb-14">
      <div
        className="text-center max-w-3xl 
                   text-3xl md:text-5xl font-semibold leading-snug
                   text-gray-900"
        style={{ wordSpacing: "0.45rem" }}
        dangerouslySetInnerHTML={{ __html: typed }}
      />

      {!done && (
        <div className="fixed inset-0 z-50 bg-white/0 pointer-events-none" />
      )}
    </div>
  );
}
