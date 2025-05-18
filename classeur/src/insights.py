import pandas as pd
import plotly.express as px
import plotly.io as pio
import re

# === CONFIG ===
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRb5MAD9HsInwz_7HqXMszLn0PQ7IOHwEvgTPBQserJCQ8Q8KS-UQoI7bIJIuDtnXJ274AUBP9zOH_N/pub?output=csv"
output_file = "insights_report.html"
pseudo_col = "Pseudo"

# === LOAD DATA ===
df = pd.read_csv(url)
df.columns = df.columns.str.strip()

figs = []

# === 1. ALIEN TASTE AWARD ===
contrarian_score = {}
categorical_cols = [
    "Nitro user? be honest",
    "Which cuisine do you prefer the most?",
    "Do you prefer sweet or savory breakfast?",
    "How often do you eat out in a week?",
    "Which pasta dish do you like the most?",
    "What kind of texture do you enjoy in food?",
    "Pineapple on pizza?",
    "Fruit cakes?",
    "Udon or Ramen?",
    "café ou thé ?"
]

for col in categorical_cols:
    if col in df.columns:
        mode_val = df[col].mode().iloc[0]
        for idx, val in df[col].items():
            pseudo = df.at[idx, pseudo_col]
            if pd.isna(pseudo) or pd.isna(val): continue
            contrarian_score[pseudo] = contrarian_score.get(pseudo, 0) + (val != mode_val)

alien_df = pd.DataFrame(list(contrarian_score.items()), columns=["Pseudo", "Contrarian Score"])
alien_df = alien_df.sort_values("Contrarian Score", ascending=False)

most_contrarian = alien_df.iloc[0]["Pseudo"]
figs.append(px.bar(alien_df, x="Pseudo", y="Contrarian Score",
                   title=f"🛸 Alien Taste Award — Most Contrarian Taster: {most_contrarian}"))


# === 2. CUISINE VS SPICY PREFERENCE ===
if "Which cuisine do you prefer the most?" in df.columns and "Rate how much you like spicy food" in df.columns:
    group = df[["Which cuisine do you prefer the most?", "Rate how much you like spicy food"]].dropna()
    group["Rate"] = pd.to_numeric(group["Rate how much you like spicy food"], errors="coerce")

    group["Cuisine"] = group["Which cuisine do you prefer the most?"].str.extract(r"(Japanese|French|Italian|Indian|Middle Eastern|South Indian|Vietnamese|Mexican|idk)", expand=False)
    group = group.dropna()

    grouped = group.groupby("Cuisine")["Rate"].mean().reset_index()
    figs.append(px.bar(grouped, x="Cuisine", y="Rate",
                       title="🌶️ Cuisine vs Average Spicy Tolerance", labels={"Rate": "Avg Spicy Rating"}))

# === 3. SWEET BREAKFAST VS FRUIT CAKE ===
if "Do you prefer sweet or savory breakfast?" in df.columns and "Fruit cakes?" in df.columns:
    filtered = df[["Do you prefer sweet or savory breakfast?", "Fruit cakes?"]].dropna()
    crosstab = pd.crosstab(filtered["Do you prefer sweet or savory breakfast?"],
                           filtered["Fruit cakes?"], normalize="index") * 100
    melted = crosstab.reset_index().melt(id_vars="Do you prefer sweet or savory breakfast?",
                                         var_name="Fruit cakes?", value_name="Percentage")
    figs.append(px.bar(melted, x="Do you prefer sweet or savory breakfast?", y="Percentage", color="Fruit cakes?",
                       barmode="group", title="🍓 Sweet Breakfast Fans vs Fruit Cake Preference"))

# === 4. PASTA FANBASE ANALYSIS ===
if "Which pasta dish do you like the most?" in df.columns:
    pasta_pref = df["Which pasta dish do you like the most?"]

    # % Lasagna fans
    lasagna_pct = (pasta_pref == "Lasagna").mean() * 100

    # % Dislike Aglio Olio (i.e., chose anything else)
    aglio_pct = (pasta_pref != "Aglio Olio").mean() * 100

    fanbase_df = pd.DataFrame({
        "Preference": ["Likes Lasagna", "Dislikes Aglio Olio"],
        "Percentage": [round(lasagna_pct, 2), round(aglio_pct, 2)]
    })
    figs.append(px.bar(fanbase_df, x="Preference", y="Percentage",
                       title="🍝 Pasta Fanbase: Lasagna & Aglio Olio Sentiment"))

    # 🧍 Carbonara fans
    carbonara_fans = df[df["Which pasta dish do you like the most?"].str.contains("Carbonara", na=False)]
    if not carbonara_fans.empty:
        fan_names = ", ".join(carbonara_fans["Pseudo"].dropna().astype(str).tolist())
        print(f"👉 People who like Carbonara: {fan_names}")

# === 5. FOOD ALIGNMENT SCORE ===
alignment = {}
for idx, row in df.iterrows():
    pseudo = row.get(pseudo_col)
    if not pseudo or pd.isna(pseudo): continue
    match = 0
    total = 0
    for col in categorical_cols:
        if col in df.columns:
            mode_val = df[col].mode().iloc[0]
            val = row.get(col)
            if pd.notna(val):
                total += 1
                if val == mode_val:
                    match += 1
    if total > 0:
        alignment[pseudo] = round((match / total) * 100, 2)

align_df = pd.DataFrame(list(alignment.items()), columns=["Pseudo", "Alignment %"])
align_df = align_df.sort_values("Alignment %", ascending=False)

most_based = align_df.iloc[0]["Pseudo"]
figs.append(px.bar(align_df, x="Pseudo", y="Alignment %",
                   title=f"🧭 Food Alignment Score — Most Based: {most_based}"))

# === SAVE OUTPUT ===
with open(output_file, "w", encoding="utf-8") as f:
    for fig in figs:
        f.write(pio.to_html(fig, full_html=False, include_plotlyjs="cdn"))

print(f"✅ Saved to {output_file}")