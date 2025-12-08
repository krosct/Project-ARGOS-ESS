import React, { useState } from "react";
import Sidebar from "./components/Sidebar";
import AnimatedIntro from "./components/AnimatedIntro";
import CheckPanel from "./components/CheckPanel";
import HistoryPanel from "./components/HistoryPanel";
import { HistoryProvider } from "./hooks/useHistory";

export default function App() {
  const [view, setView] = useState("new");

  return (
    <HistoryProvider>
      <div className="min-h-screen flex bg-white text-black">
        <Sidebar view={view} setView={setView} />

        <main className="flex-1 flex justify-center items-start p-6 md:p-10">
          <div className="w-full max-w-4xl flex flex-col items-center gap-16">
            {/* Intro aparece apenas na aba "new" */}
            {view === "new" && (
              <div className="w-full flex justify-center">
                <AnimatedIntro />
              </div>
            )}

            {/* Painéis */}
            <div className="w-full">
              {view === "new" ? <CheckPanel /> : <HistoryPanel />}
            </div>
          </div>
        </main>
      </div>
    </HistoryProvider>
  );
}
