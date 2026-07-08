import networkx as nx
from pyvis.network import Network


# Utility: normalize person names (ensure consistent keys)
def normalize(name):
    if not isinstance(name, str):
        return name
    return name.strip()

# ============================================================
# PEOPLE & COUNTRIES
# ============================================================

people = {
    "Pata": "Quebec",
    "Ruy": "Canada",
    "Svet": "France",
    "Celsia": "USA",
    "Aquila": "New Zealand",
    "Hex": "France",
    "James": "Quebec",
    "Nia": "Canada",

    "Damocles": "France",
    "Cokolita": "Serbia",
    "Mari": "Serbia",

    "Limou": "USA",
    "Darian": "France",

    "Andy": "France",
    "Neil": "Philippines",
    "Hassan": "France",

    "G-Admin": "Germany",

    "Wemily": "Switzerland",

    "Albatros": "Canada",
    "Existence": "Canada",

    "River": "Luxembourg",
    "Donut": "USA",
    "Pile": "Unknown",
    "Ned": "France",
    "Roto": "France",
    "Shae": "France",
    "Dimirah": "Unknown",

    "Vyn": "Philippines",
    "Soro": "France",

    "Mylene": "Montenegro",
}

# ============================================================
# COUNTRY COLOURS
# ============================================================

country_colors = {
    "Canada": "#ff4d4d",
    "Quebec": "#4d5fff",
    "France": "#4da6ff",
    "USA": "#ff4dac",
    "Serbia": "#b266ff",
    "Germany": "#ffd24d",
    "Switzerland": "#ff944d",
    "Philippines": "#4dfff3",
    "New Zealand": "#ff69b4",
    "Luxembourg": "#00c851",
    "Montenegro": "#00b7c8",
    "Unknown": "#c0c0c0",
}

# ============================================================
# PERSON -> PEOPLE THEY HAVE MET
# ============================================================

host_meetups = {

    "Pata": [
        "Aquila",
        "James",
        "Svet",
        "Nia",
        "Hex",
        "Celsia",
        "Ruy",
    ],

    "Celsia": [
        "Damocles",
        "Aquila",
        "Hex",
        "Svet",
        "Nia",
        "Ruy",
        "Pata",
        "Roto",
        "Shae",
        "Albatros",
        "Dimirah",
        "Andy",
        "G-Admin",
        "Donut",
        "River",
        "Ned",
        "Pile",
    ],

    "Limou": [
        "Darian",
    ],

    "Cokolita": [
        "Mari",
        "Svet",
        "Damocles",
        "Celsia",
        "Dimirah",
    ],

    "Mylene": [
        "Dimirah",
    ],
    
    "Vyn": [
        "Soro",
    ],
    
    "Hex": [
        "Aquila",
        "Svet",
        "Celsia",
        "Pata",
        "Ruy",
        "Dimirah",
    ],
    
    "Aquila": [
        "Hex",
        "Svet",
        "Celsia",   
        "Pata",
        "Ruy",
        "James",
        "Existence",
        "Dimirah",
    ],

    "Svet": [

        "Wemily",
        "Neil",
        "Hassan",
        
        "Andy",
        "Albatros",

        "Pata",
        "Nia",
        "Aquila",

        "Existence",

        "Dimirah",

        "James",

        "Hex",

        "Cokolita",
        "Mari",

        "Celsia",     
        "Damocles",
    ],
    
    "Existence": [
        "Aquila",
        "James",
        "Pata",  
    ] 
}

# ============================================================
# COUPLES
# ============================================================

couples = {
    ("Pata", "Ruy"),
    ("Svet", "Cokolita"),
    ("Damocles", "Celsia"),
    ("Hex", "Aquila"),
    ("Vyn", "Soro"),
}

# ============================================================
# BUILD GRAPH
# ============================================================

G = nx.Graph()

for host, guests in host_meetups.items():

    host = normalize(host)

    G.add_node(host)

    for guest in guests:

        guest = normalize(guest)

        G.add_node(guest)

        if G.has_edge(host, guest):
            G[host][guest]["weight"] += 1
        else:
            G.add_edge(host, guest, weight=1)

# ============================================================
# NETWORK STATISTICS
# ============================================================

degree = dict(G.degree())
betweenness = nx.betweenness_centrality(G)

# ============================================================
# CREATE NETWORK
# ============================================================

net = Network(
    height="900px",
    width="100%",
    bgcolor="#1b1b1b",
    font_color="white",
)

net.force_atlas_2based()

# ============================================================
# ADD NODES
# ============================================================

for node in G.nodes():

    country = people.get(node, "Unknown")

    colour = country_colors.get(country, "#c0c0c0")

    title = (
    f"{node}\n"
    f"{country}\n"
    f"Connections: {degree[node]}\n"
    f"Bridge Score: {betweenness[node]:.3f}"
    )

    size = 18 + degree[node] * 4

    net.add_node(
        node,
        label=node,
        title=title,
        color=colour,
        size=size,
    )

# ============================================================
# ADD EDGES
# ============================================================

for u, v, data in G.edges(data=True):

    weight = data["weight"]

    is_couple = (
        (u, v) in couples or
        (v, u) in couples
    )

    if is_couple:

        net.add_edge(
            u,
            v,
            value=weight + 4,
            color="red",
            width=5,
            title=f"❤️ En couple",
        )

    else:

        net.add_edge(
            u,
            v,
            value=weight,
            color="#999999",
            width=1 + weight,
            title=f"Met {weight} time(s)"
        )

# ============================================================
# PHYSICS
# ============================================================

net.set_options("""
{
  "nodes": {
    "borderWidth": 2,
    "font": {
      "size": 18
    }
  },

  "edges": {
    "smooth": {
      "enabled": true,
      "type": "dynamic"
    }
  },

  "physics": {

    "forceAtlas2Based": {

      "gravitationalConstant": -90,
      "springLength": 170,
      "springConstant": 0.02

    },

    "solver": "forceAtlas2Based",

    "minVelocity": 0.75

  }
}
""")

# ============================================================
# SAVE
# ============================================================

net.write_html(
    "meetups.html",
    notebook=False,
    open_browser=True
)

print("\nSaved to meetups.html")

# ============================================================
# STATISTICS
# ============================================================

print("\n==============================")
print("Most Connected Members")
print("==============================")

for person, deg in sorted(
    degree.items(),
    key=lambda x: x[1],
    reverse=True,
):
    print(f"{person:<15} {deg}")

print("\n==============================")
print("Bridge Members")
print("==============================")

for person, score in sorted(
    betweenness.items(),
    key=lambda x: x[1],
    reverse=True,
):
    print(f"{person:<15} {score:.3f}")