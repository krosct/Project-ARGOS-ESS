import React, { useEffect, useState } from "react";
import useTypewriter from "../hooks/useTypewriter";

export default function AnimatedIntro() {
  const introText =
    "Em mundo cada vez mais hauhauha polarizado, nosso objetivo é detectar notícias falsas de forma imparcial, vamos analisar sua dúvida agora.";
  const highlightText = "detectar notícias falsas de forma imparcial";
  const [done, setDone] = useState(false);
  const typed = useTypewriter(introText, {
    speed: 30,
    highlight: highlightText,
    onDone: () => setDone(true),
  });

  return (
    <div className="w-full flex flex-col items-center">
      <div
        className={`animated-intro text-center max-w-8xl`}
        dangerouslySetInnerHTML={{ __html: typed }}
      />
      {!done && (
        <div className="fixed inset-0 z-50 bg-white/0" aria-hidden="true" />
      )}
    </div>
  );
}
