import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Replace with your Google Sheet direct .xlsx link (published or with access)
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRb5MAD9HsInwz_7HqXMszLn0PQ7IOHwEvgTPBQserJCQ8Q8KS-UQoI7bIJIuDtnXJ274AUBP9zOH_N/pub?output=csv"

df = pd.read_csv(url)
df.columns = df.columns.str.strip()

figs = []

# 1. Nitro
figs.append(px.pie(df, names="Nitro user? be honest", title="💥 Nitro User Honesty"))

# 2. Favorite Cuisine
figs.append(px.pie(df, names="Which cuisine do you prefer the most?", title="🍱 Favorite Cuisine"))

# 3. Spicy Food Tolerance by Pseudo
spice = df[["Pseudo", "Rate how much you like spicy food"]].dropna()
spice["Rate"] = pd.to_numeric(spice["Rate how much you like spicy food"], errors="coerce")
figs.append(px.bar(spice, x="Pseudo", y="Rate", title="🌶️ Spicy Tolerance by Pseudo"))

# 4. Sweet vs Savory
figs.append(px.pie(df, names="Do you prefer sweet or savory breakfast?", title="🍳 Sweet or Savory Breakfast"))

# 5. Eat Out
figs.append(px.pie(df, names="How often do you eat out in a week?", title="💸 Eat Out Frequency"))
eat_out = df[["Pseudo", "How often do you eat out in a week?"]].dropna()
eat_out["Count"] = pd.to_numeric(eat_out["How often do you eat out in a week?"], errors="coerce")
figs.append(px.line(eat_out, x="Pseudo", y="Count", title="💸 Eat Out by Pseudo (Spending Ranking)"))

# 6. Dessert Ranks
desserts = [
    "Ice cream", "Cheesecake", "Brownies", "Tiramisu", "Macarons", "Chocolatine"
]
for dessert in desserts:
    col = f"Rank these desserts from most to least favorite   [{dessert}]"
    if col in df.columns:
        figs.append(px.histogram(df, x=col, title=f"🍰 Dessert Rank - {dessert}"))

# 7. Pasta Dish + filter pseudos
figs.append(px.pie(df, names="Which pasta dish do you like the most?", title="🍝 Pasta Preferences"))

# 8. Texture
figs.append(px.histogram(df, x="What kind of texture do you enjoy in food?", title="🧂 Texture Preferences"))

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