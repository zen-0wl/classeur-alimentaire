import React, { useEffect, useState } from "react";
import Papa from "papaparse";

const sheetUrl =
  "https://docs.google.com/spreadsheets/d/e/2PACX-1vRb5MAD9HsInwz_7HqXMszLn0PQ7IOHwEvgTPBQserJCQ8Q8KS-UQoI7bIJIuDtnXJ274AUBP9zOH_N/pub?output=csv";

const Leaderboard = () => {
  const [leaderboard, setLeaderboard] = useState([]);

  useEffect(() => {
    Papa.parse(sheetUrl, {
      download: true,
      header: true,
      complete: (results) => {
        const data = results.data;
        const scores = {};

        data.forEach((row, idx) => {
          const pseudo = row.Pseudo || `anon_${idx}`;
          if (!pseudo) return;

          let score = 0;

          // Nitro
          score += row["Nitro user? be honest"] === "Yes onee-sama" ? 10 : row["Nitro user? be honest"] === "N-no" ? 6 : 0;

          // Cuisine
          const cuisine = row["Which cuisine do you prefer the most?"];
          if (cuisine === "Vietnamese") score += 10;
          else if (cuisine === "Japanese") score += 8;
          else if (["Italian", "Middle Eastern"].includes(cuisine)) score += 6;
          else score += 4;

          // Spicy food rate
          const spicy = parseInt(row["Rate how much you like spicy food"]);
          if (spicy === 5) score += 10;
          else if (spicy === 4) score += 9;
          else if (!isNaN(spicy)) score += 5;

          // Sweet or savory
          const mood = row["Do you prefer sweet or savory breakfast?"]?.toLowerCase();
          if (mood === "depends on the mood") score += 12;
          else if (mood === "savory") score += 10;
          else score += 8;

          // Eat out
          const eat = row["How often do you eat out in a week?"];
          if (eat === "4-5 times") score += 12;
          else if (eat === "3-4 times") score += 10;
          else score += 7;

          // Dessert ranks
          const firstRank = {
            Brownies: 10,
            Tiramisu: 9,
            Chocolatine: 9,
            Macarons: 7,
            Cheesecake: 6,
            "Ice cream": 8,
          };
          const secondRank = {
            Brownies: 9,
            Tiramisu: 8,
            Chocolatine: 8,
            Macarons: 7,
            Cheesecake: 5,
            "Ice cream": 7,
          };
          Object.keys(firstRank).forEach((dessert) => {
            const col = `Rank these desserts from most to least favorite   [${dessert}]`;
            const rank = parseInt(row[col]);
            if (rank === 1) score += firstRank[dessert];
            if (rank === 2) score += secondRank[dessert];
          });

          // Pasta dish
          const pasta = row["Which pasta dish do you like the most?"];
          if (pasta === "Carbonara") score += 8;
          else if (pasta === "Lasagna") score += 10;
          else if (pasta === "Aglio Olio") score += 7;
          else if (pasta === "Pesto") score += 5;
          else if (pasta === "Bolognese") score += 7;

          // Texture
          const texture = row["What kind of texture do you enjoy in food?"] || "";
          if (texture.includes("Crunchy") || texture.includes("Crispy")) score += 12;
          else if (texture.includes("Creamy")) score += 10;
          else score += 6;

          // Spicy & Sweet
          const spiceSweet = parseInt(row["If a dish is both spicy and sweet, how likely are you to enjoy it?"]);
          score += spiceSweet === 5 ? 10 : !isNaN(spiceSweet) ? 2 : 0;

          // Food factor
          const factor = row["When choosing food, what matters more?"];
          score += { Taste: 10, Price: 9, Convenience: 2, Nutrition: 2 }[factor] || 0;

          // Pineapple
          score += { NAY: 18, Maybe: 0 }[row["Pineapple on pizza?"]] || 0;

          // Poutine
          score += { YAY: 18, "aspie me deteste": 4 }[row["Poutine?"]] || 0;

          // Fruit cakes
          score += { NAY: 18, Maybe: 2 }[row["Fruit cakes?"]] || 0;

          // Udon vs Ramen
          score += { Ramen: 18, Both: 15, Udon: 12 }[row["Udon or Ramen?"]] || 0;

          // Café ou Thé
          score += row["café ou thé ?"] === "thé" ? 20 : 0;

          scores[pseudo] = score;
        });

        const leaderboardArray = Object.entries(scores)
          .map(([pseudo, score]) => ({ pseudo, score }))
          .sort((a, b) => b.score - a.score)
          .map((entry, index) => ({
            Rank: index + 1,
            Pseudo: entry.pseudo,
            Score: entry.score,
            Award: [
              "🥇 Ultimate Gourmet",
              "🥈 Refined Palate",
              "🥉 Dessert Bee",
              "🌶️ Spicer",
              "🍱 Balanced Connoisseur",
              "🍜 Noodle Nomad",
              "🍍 Pineapple Purist",
              "🍓 Cake Avenger",
              "🍝 Pasta Undertaker",
              "☕ Zen of Flavour",
            ][index] || "🍴 Foodie (Actual Normie)",
          }));

        setLeaderboard(leaderboardArray);
      },
    });
  }, []);

  return (
    <div className="overflow-x-auto w-full mt-4">
      <table className="min-w-full text-sm text-left">
        <thead>
          <tr className="bg-blue-100">
            <th className="py-2 px-4">Rank</th>
            <th className="py-2 px-4">Pseudo</th>
            <th className="py-2 px-4">Score</th>
            <th className="py-2 px-4">Award</th>
          </tr>
        </thead>
        <tbody>
          {leaderboard.map((entry) => (
            <tr key={entry.Pseudo} className="border-b hover:bg-gray-100">
              <td className="py-2 px-4 font-semibold">{entry.Rank}</td>
              <td className="py-2 px-4">{entry.Pseudo}</td>
              <td className="py-2 px-4">{entry.Score}</td>
              <td className="py-2 px-4">{entry.Award}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Leaderboard;