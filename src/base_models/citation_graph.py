import sys
import cudf
import cugraph
import pickle
import pandas as pd

def default_factory():
    return list()
with open("data/zbRevQual_cit/zbl_cit_bw.pickle", "rb") as f:
    backwarddict = pickle.load(f)
backwarddict = {k: v for k, v in backwarddict.items() if v}
backwarddict = {k: [x for x in v if x != k] for k, v in backwarddict.items()}
with open("data/zbRevQual_cit/zbl_cit_fw.pickle", "rb") as f:
    forwardcit = pickle.load(f)
forwardcit = {k: v for k, v in forwardcit.items() if v}
forwardcit = {k: [x for x in v if x != k] for k, v in forwardcit.items()}

backwarddict = {k: v for k, v in backwarddict.items() if v}
forwardcit = {k: v for k, v in forwardcit.items() if v}

# ----------------------------
# 1) Build a unified edgelist (deduplicated) + full node set (to count isolates)
# ----------------------------
edges = set()

# From forward citations: src -> dst
for src, dsts in forwardcit.items():
    for dst in dsts:
        edges.add((src, dst))

# From backward citations: each citer -> the key (dst)
for dst, citers in backwarddict.items():
    for src in citers:
        edges.add((src, dst))

# Nodes: union of keys and values from both dicts
all_nodes = set(forwardcit.keys()) | set(backwarddict.keys())
all_nodes |= {v for vs in forwardcit.values() for v in vs}
all_nodes |= {v for vs in backwarddict.values() for v in vs}

# ----------------------------
# 2) Move edgelist to GPU (cuDF)
# ----------------------------
# Note: directedness is expressed by edge order (src -> dst)
edges_gdf = cudf.DataFrame(list(edges), columns=["src", "dst"])


# ----------------------------
# 3) Construct a DIRECTED graph in cuGraph
# ----------------------------
# This is where you specify that the graph is directed: use DiGraph()
G = cugraph.Graph(directed=True)
# renumber=False keeps your IDs as-is (strings/ints). If your IDs are strings,
# set renumber=True to get better performance, and map back if needed.
G.from_cudf_edgelist(edges_gdf, source="src", destination="dst", renumber=True)

external_ids = cudf.Series(['1004.16022', '1307.14002'])
# Get the internal node IDs corresponding to the external IDs
internal_ids = G.lookup_internal_vertex_id(external_ids)
# Show the result
print(" internal_ids: ", internal_ids)

print(f"GPU graph has {int(G.number_of_vertices())} vertices (non-isolated only) and {int(G.number_of_edges())} edges.")

# ---- Weakly Connected Components (ignores edge direction for connectivity) ----
Gu = cugraph.Graph()  # undirected
Gu.from_cudf_edgelist(edges_gdf, source="src", destination="dst", renumber=True)
wcc = cugraph.weakly_connected_components(Gu)  # columns: ['vertex','labels']

# size per component
sizes = wcc.groupby("labels").size().reset_index().rename(columns={0: "size"})

num_components = int(len(sizes))                      # total components present
num_nontrivial_components = int((sizes["size"] >= 2).sum())  # components with >=2 vertices
largest_size = int(sizes["size"].max())
size_counts = sizes['size'].value_counts().sort_index()
# Count “smaller graphs” as all components except the largest (giant component)
num_smaller_than_giant = int((sizes["size"] < largest_size).sum())
#print("All sizes: ", sizes)
print({
    "num_components_total": num_components,
    "num_nontrivial_components_(size>=2)": num_nontrivial_components,
    "largest_component_size": largest_size,
    "num_components_excluding_giant": num_smaller_than_giant
})
size_counts = sizes['size'].value_counts().sort_index()
print("Frequency of sizes: ", size_counts)

# ----------------------------
# 5) Shortest path between two nodes
# ----------------------------
# A) Unweighted shortest path: use BFS; then reconstruct the path
source = internal_ids.iloc[0]
print("source type: ", type(source))
target = internal_ids.iloc[1]

if source not in G.nodes() or target not in G.nodes():
    print("Source or target not in the graph.")

print("short path len; ", cugraph.bfs_edges(G, 846527))
shortest_path_df = cugraph.shortest_path(G, source=source)
print("shortest_path_df: ", shortest_path_df)
# ----------------------------
# 6) Save & reload
# ----------------------------
# Save the edgelist for future reuse (recommended for cuGraph)
edges_gdf.to_parquet("citation_edges.parquet", index=False)

# Reload later:
edges_gdf2 = cudf.read_parquet("citation_edges.parquet")
G2 = cugraph.Graph()
G2.from_cudf_edgelist(edges_gdf2, source="src", destination="dst", renumber=True)
print("Reloaded GPU graph edges:", int(G2.number_of_edges()))
