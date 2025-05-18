import re
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRb5MAD9HsInwz_7HqXMszLn0PQ7IOHwEvgTPBQserJCQ8Q8KS-UQoI7bIJIuDtnXJ274AUBP9zOH_N/pub?output=csv"

df = pd.read_csv(url)
df.columns = df.columns.str.strip()

figs = []

# 1. Nitro
figs.append(px.pie(df, names="Nitro user? be honest", title="✧˖° Nitro User Honesty"))

# 2. Favorite Cuisine
figs.append(px.pie(df, names="Which cuisine do you prefer the most?", title="🍱 Favourite Cuisine"))

# 3. Spicy Food Tolerance by Pseudo
spice_col = "Rate how much you like spicy food"
if "Pseudo" in df.columns and spice_col in df.columns:
    spice = df[["Pseudo", spice_col]].dropna()
    spice["Rate"] = pd.to_numeric(spice[spice_col], errors="coerce")
    fig = go.Figure()
    fig.add_trace(go.Bar(x=spice["Pseudo"], y=spice["Rate"], name="Bar", marker_color="salmon"))
    fig.add_trace(go.Scatter(x=spice["Pseudo"], y=spice["Rate"], name="Line", mode="lines+markers", line=dict(color="firebrick")))
    fig.update_layout(title="🌶️ Spicy Tolerance by Pseudo", xaxis_tickangle=-45)
    figs.append(fig)

# 4. Sweet vs Savory
figs.append(px.pie(df, names="Do you prefer sweet or savory breakfast?", title="🍳 Sweet or Savory Breakfast"))

# 5. Eat Out
figs.append(px.pie(df, names="How often do you eat out in a week?", title="💸 Eat Out Frequency"))

eat_out_col = "How often do you eat out in a week?"
if "Pseudo" in df.columns and eat_out_col in df.columns:
    eat_out = df[["Pseudo", eat_out_col]].dropna()

    # Convert string answers to numeric scores
    eating_out_map = {
        "Daily (riche parisian vibes)": 4,
        "4-5 times": 3,
        "3-4 times": 2,
        "2-3 times": 1,
        "0-1 times": 0,
    }
    eat_out["Score"] = eat_out[eat_out_col].map(eating_out_map)

    # Drop entries with unknown mappings
    eat_out = eat_out.dropna(subset=["Score"])

    # Plot bar + line chart
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=eat_out["Pseudo"],
        y=eat_out["Score"],
        name="Spending Score (Bar)",
        marker_color="lightgreen"
    ))
    fig.add_trace(go.Scatter(
        x=eat_out["Pseudo"],
        y=eat_out["Score"],
        name="Trend Line",
        mode="lines+markers",
        line=dict(color="darkgreen")
    ))
    fig.update_layout(
        title="💸 Eat Out by Pseudo (Spending Score Ranking)",
        xaxis_title="Pseudo",
        yaxis_title="Score",
        xaxis_tickangle=-45
    )
    figs.append(fig)

# 6. Dessert Ranks
# desserts = [
#     "Ice cream", "Cheesecake", "Brownies", "Tiramisu", "Macarons", "Chocolatine"
# ]
# for dessert in desserts:
#     col = f"Rank these desserts from most to least favorite   [{dessert}]"
#     if col in df.columns:
#         figs.append(px.histogram(df, x=col, title=f"🍰 Dessert Rank - {dessert}"))

dessert_cols = {
    "Ice cream": "Rank these desserts from most to least favorite   [Ice cream]",
    "Cheesecake": "Rank these desserts from most to least favorite   [Cheesecake]",
    "Brownies": "Rank these desserts from most to least favorite   [Brownies]",
    "Tiramisu": "Rank these desserts from most to least favorite   [Tiramisu]",
    "Macarons": "Rank these desserts from most to least favorite   [Macarons]",
    "Chocolatine": "Rank these desserts from most to least favorite   [Chocolatine]"
}

rank_weights = {1: 6, 2: 5, 3: 4, 4: 3, 5: 2, 6: 1}

def extract_rank(value):
    match = re.match(r"(\d+)", str(value))
    return int(match.group(1)) if match else None

weighted_scores = {}

for dessert, col in dessert_cols.items():
    if col in df.columns:
        # Apply rank extractor
        ranks = df[col].dropna().apply(extract_rank).dropna()
        score = 0
        for rank_value, weight in rank_weights.items():
            count = (ranks == rank_value).sum()
            score += count * weight
        weighted_scores[dessert] = score

score_df = pd.DataFrame(list(weighted_scores.items()), columns=["Dessert", "Score"])
score_df = score_df.sort_values("Score", ascending=False)

fig = px.bar(
    score_df,
    x="Dessert",
    y="Score",
    title="🍰 Overall Dessert Ranking (Weighted by Votes)",
    text="Score",
    color="Score",
    color_continuous_scale="Blues"
)
fig.update_layout(yaxis_title="Weighted Score", xaxis_title="Dessert")
figs.append(fig)

# 7. Pasta Dish + filter pseudos
figs.append(px.pie(df, names="Which pasta dish do you like the most?", title="🍝 Pasta Preferences"))

# 8. Texture
texture_col = [col for col in df.columns if "texture" in col.lower()][0]

keywords = ["Crunchy", "Creamy", "Chewy", "Juicy", "Crispy", "Soft"]
texture_counts = {k: 0 for k in keywords}

# Parse checkbox-style multi-answers
for val in df[texture_col].dropna():
    choices = [choice.strip().capitalize() for choice in val.split(",")]
    for choice in choices:
        if choice in texture_counts:
            texture_counts[choice] += 1

# Prepare DataFrame
texture_df = pd.DataFrame(texture_counts.items(), columns=["Texture", "Count"])
texture_df = texture_df.sort_values("Count", ascending=True)

# Plot horizontal bar chart
fig = px.bar(
    texture_df,
    x="Count",
    y="Texture",
    orientation="h",
    title="🧂 Texture Preferences",
    text="Count",
    color_discrete_sequence=["mediumpurple"]
)
fig.update_layout(xaxis_title="Responses", yaxis_title="", title_font_size=22)
figs.append(fig)

# 9. Spicy + Sweet
figs.append(px.histogram(df, x="If a dish is both spicy and sweet, how likely are you to enjoy it?", title="🌶️+🍬 Combo Taste Preference"))

# 10. Choosing Food Factors
figs.append(px.pie(df, names="When choosing food, what matters more?", title="🛒 What Matters Most When Choosing Food"))

# 11. Pineapple on Pizza
figs.append(px.pie(df, names="Pineapple on pizza?", title="🍍 Pineapple on Pizza"))

# 12. Poutine
figs.append(px.pie(df, names="Poutine?", title="🍟 Poutine"))

# 13. Fruit Cakes
figs.append(px.pie(df, names="Fruit cakes?", title="🍓 Fruit Cakes"))

# 14. Udon or Ramen
figs.append(px.pie(df, names="Udon or Ramen?", title="🍜 Udon or Ramen"))

# 15. Café ou Thé
figs.append(px.pie(df, names="café ou thé ?", title="☕ Café ou Thé ?"))

# Save all visuals into one HTML
with open("visual_report.html", "w", encoding="utf-8") as f:
    for fig in figs:
        f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))