import React, { useState } from "react";
import VisualEmbed from "./components/results";
import Leaderboard from "./components/leaderboard";

function App() {
  const [activeTab, setActiveTab] = useState("results");

  return (
    <div className="min-h-screen flex flex-col text-gray-800 font-sans">
      <header className="sticky top-0 bg-white bg-opacity-90 backdrop-blur-md shadow-md py-4 z-50">
        <h1 className="text-4xl font-bold text-center">🍽️ Interprétations Alimentaires</h1>
        <p className="text-center text-sm text-gray-600">
          Visualisez les préférences alimentaires et découvrez le classement des gourmets !
        </p>
        <nav className="flex justify-center gap-4 mt-4">
          <button
            className={`px-5 py-2.5 rounded-full font-semibold transition ${
              activeTab === "results"
                ? "bg-blue-500 text-white"
                : "bg-gray-200 text-gray-700 hover:bg-blue-100"
            }`}
            onClick={() => setActiveTab("results")}
          >
            Visual Results
          </button>
          <button
            className={`px-5 py-2.5 rounded-full font-semibold transition ${
              activeTab === "leaderboard"
                ? "bg-blue-500 text-white"
                : "bg-gray-200 text-gray-700 hover:bg-blue-100"
            }`}
            onClick={() => setActiveTab("leaderboard")}
          >
            🏆 Leaderboard
          </button>
        </nav>
      </header>

      <div className="flex-1 w-screen overflow-hidden">
        {activeTab === "results" ? (
          <div className="w-full h-full">
            <VisualEmbed />
          </div>
        ) : (
          <main className="bg-white rounded-xl shadow-md p-6 m-6 max-w-5xl mx-auto">
            <Leaderboard />
          </main>
        )}
      </div>

      {/* Spacer */}
      <div style={{ height: "2rem" }} />

      <footer className="text-center text-sm text-gray-500 py-4">
        — zen`` · {new Date().getFullYear()}
      </footer>
    </div>
  );
}

export default App;