import os
import sys
import numpy as np
import pandas as pd
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import homogeneity_completeness_v_measure,silhouette_score

CONN_CUTOFF = 0.5

infile = sys.argv[1]
use_conn = bool(int(sys.argv[2]))
use_ed  = bool(int(sys.argv[3]))

def cluster(df, a, k, use_ed):
    a.set_params(n_clusters=k)
    if use_ed:
        a.fit(df)
    else:
       a.fit(1 - df)
 
    return a.labels_

def get_connectivity_matrix(df, cutoff=0.5):
    if df.shape[0] != df.shape[1]:
        raise ValueError("Expecting square DataFrame")
    if list(df.index) != list(df.columns):
        raise ValueError("Expecting same order of rows and columns")
    
    conn = df.values.copy()
    a = np.zeros((df.shape[0], df.shape[0]))
    a[np.diag_indices(df.shape[0])] = 1
    conn[conn >= cutoff] = 1
    conn[conn < cutoff] = 0
    conn[a.astype(bool)] = 0
    return conn

sys.stderr.write("Reading table\n")
df = pd.read_table(infile, index_col=0)
sys.stderr.write("Done\n")

df = df.loc[sorted(df.columns),sorted(df.columns)]
conn = None 
if use_conn:
    conn = get_connectivity_matrix(df, CONN_CUTOFF)

cluster_start = 2
cluster_end = df.shape[0]

if use_ed:
    a = AgglomerativeClustering(
        memory="/tmp/", compute_full_tree=True, 
        connectivity=conn,
        )
else:
    a = AgglomerativeClustering(
        affinity="precomputed", 
        linkage="complete", connectivity=conn,
        memory="/tmp/", compute_full_tree=True, 
        )

print("\t{}".format("\t".join(df.columns)))
for k in range(cluster_start, cluster_end):
    sys.stderr.write("{}\n".format(k))
    labels = cluster(df, a, k, use_ed)
    print("{}\t{}".format(k, "\t".join([str(x) for x in labels])))
