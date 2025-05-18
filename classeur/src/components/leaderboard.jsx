import useSheetData from "../data/sheetdata";

const csvUrl = "https://docs.google.com/spreadsheets/d/15pEMNUekcMbwJ9HhN2ju422on8ShuzHmupsUzvjweJg/edit?usp=sharing";

const calculateScore = (row) => {
  let score = 0;
  if (row["Which cuisine do you prefer the most?"] === "Japanese") score += 5;
  if (parseInt(row["Rate how much you like spicy food"], 10) >= 8) score += 3;
  if (row["Do you prefer sweet or savory breakfast?"] === "Savory") score += 2;
  return score;
};

function Leaderboard() {
  const data = useSheetData(csvUrl);

  const scoredData = data.map((row) => ({
    name: row["Name (or Nickname)"],
    score: calculateScore(row),
  }))
    .filter(d => d.name)
    .sort((a, b) => b.score - a.score);

  return (
    <div className="overflow-x-auto">
      <h2 className="text-xl font-semibold mb-6 text-center">🏆 Leaderboard Rankings</h2>
      <table className="min-w-full table-auto border border-gray-300 shadow-sm">
        <thead className="bg-blue-100">
          <tr>
            <th className="px-4 py-2 text-left">Rank</th>
            <th className="px-4 py-2 text-left">Name</th>
            <th className="px-4 py-2 text-left">Score</th>
          </tr>
        </thead>
        <tbody>
          {scoredData.map((entry, index) => (
            <tr key={index} className="odd:bg-white even:bg-gray-100">
              <td className="px-4 py-2">#{index + 1}</td>
              <td className="px-4 py-2">{entry.name}</td>
              <td className="px-4 py-2">{entry.score}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Leaderboard;