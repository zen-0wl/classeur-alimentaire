import React, { useEffect, useState } from "react";
import Papa from "papaparse";

const sheetUrl =
  "https://docs.google.com/spreadsheets/d/e/2PACX-1vRb5MAD9HsInwz_7HqXMszLn0PQ7IOHwEvgTPBQserJCQ8Q8KS-UQoI7bIJIuDtnXJ274AUBP9zOH_N/pub?output=csv";

 function VisualEmbed() {
  const [responses, setResponses] = useState([]);

  useEffect(() => {
    Papa.parse(sheetUrl, {
      download: true,
      header: true,
      complete: (results) => {
        const rawData = results.data;

        // Normalize headers: fix curly quotes and trim whitespace
        const cleanedData = rawData.map((row) => {
          const cleanedRow = {};
          Object.entries(row).forEach(([key, value]) => {
            const normalizedKey = key.replace(/[’‘]/g, "'").trim(); // replace curly quotes
            cleanedRow[normalizedKey] = value;
          });
          return cleanedRow;
        });

        setResponses(cleanedData);
      }
    });
  }, []);

  const openQuestions = [
    "What's your all-time favorite dish?",
    "If you could only eat one cuisine for a month, what would it be?",
    "Favorite snack?",
    "Which indulgent food do you always say yes to?",
    "Weirdest food combo you enjoy? tell your senpai da secrets",
    "What's a french dish you wish to try?"
  ];

     return (
    <div>
      {/* Top: Visual Report */}
      <iframe
        src="/visual_report.html"
        style={{
          width: "100%",
          height: "calc(100vh - 220px)", // Adjust to match header/footer size
          border: "none",
          display: "block"
        }}
        title="Food Dashboard"
      />

      {/* Spacer */}
      <div style={{ height: "2rem" }} />

      {/* Bottom: Insights Report */}
      <iframe
        src="/insights_report.html"
        style={{
          width: "100%",
          height: "calc(100vh - 220px)", // Same height as above
          border: "none",
          display: "block"
        }}
        title="Food Insights"
      />
      {/* Spacer */}
      <div style={{ height: "4rem" }} />

      {/* Open-ended Question Tables */}
      <div className="max-w-6xl mx-auto px-4 mb-20">
        <h2 className="text-2xl font-bold text-center mb-6 text-white">🎌 Open-Ended Reveals</h2>

        {openQuestions.map((question, idx) => (
          <div key={idx} className="mb-10">
            <h3 className="text-lg font-semibold text-yellow-300 mb-2">{question}</h3>
            <div className="overflow-x-auto border border-yellow-400 rounded-md">
              <table className="min-w-full text-sm text-left text-gray-800">
                <thead className="bg-yellow-200 text-black">
                  <tr>
                    <th className="py-2 px-4 border-b border-yellow-300">Responses</th>
                  </tr>
                </thead>
                <tbody>
                  {responses
                    .map((row) => row[question])
                    .filter(Boolean)
                    .map((answer, i) => (
                      <tr
                        key={i}
                        className={i % 2 === 0 ? "bg-white border-b" : "bg-yellow-50 border-b"}
                      >
                        <td className="py-2 px-4">{answer}</td>
                      </tr>
                    ))}
                </tbody>
              </table>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default VisualEmbed;