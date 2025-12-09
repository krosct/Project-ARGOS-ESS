import React, { useState } from "react";
import Sidebar from "./components/Sidebar";
import AnimatedIntro from "./components/AnimatedIntro";
import CheckPanel from "./components/CheckPanel";
import HistoryPanel from "./components/HistoryPanel";
import { HistoryProvider } from "./hooks/useHistory";

export default function App() {
  const [view, setView] = useState("new"); // 'new' | 'history'

  return (
    <HistoryProvider>
      <div className="min-h-screen flex bg-white text-black">
        <Sidebar view={view} setView={setView} />

        <main className="flex-1 flex justify-center items-start p-6">
          <div className="w-full max-w-3xl flex flex-col items-center">
            {view === "new" && <AnimatedIntro />}

            <div className="w-full mt-80 relative">
              {view === "new" && (
                <div className="panel">
                  <CheckPanel />
                </div>
              )}

              {view === "history" && (
                <div className="panel">
                  <HistoryPanel />
                </div>
              )}
            </div>
          </div>
        </main>
      </div>
    </HistoryProvider>
  );
}
