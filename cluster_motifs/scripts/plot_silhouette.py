import pandas as pd
from sklearn.metrics import silhouette_score
import seaborn as sns
import matplotlib.pyplot as plt
from multiprocessing import Pool

infile = snakemake.input[0] #"out/cluster_table.txt"
distance_file = snakemake.input[1] #"out/distance_table.txt"
outfile = snakemake.output[0] #"test.png" #snakemake
#outfile2 = snakemake.output[1] #"test.png" #snakemake
stepsize = 1

df_d = pd.read_table(distance_file, index_col=0)
df_c = pd.read_table(infile, index_col=0)

cols = sorted(df_d.columns)
df_d = df_d.loc[cols, cols]
df_c = df_c[cols]

pool = Pool()
jobs = []
for cluster,labels in df_c.iterrows():
    if cluster % stepsize != 0:
        continue
    if cluster >= 1 and cluster < df_d.shape[0]:
        job = pool.apply_async(silhouette_score, (df_d, labels.values))
        jobs.append((cluster, job))

pool.close()
pool.join()

x = []
y = []
for cluster, job in jobs:
    x.append(cluster)
    y.append(job.get())

fig = plt.figure()
plt.plot(x, y)
plt.xlabel("Cluster")
plt.ylabel("Silhouette width")
plt.savefig(outfile, dpi=300)

#pool = Pool()
#jobs = []
#for cluster,labels in df_c.iterrows():
#    if cluster % 10 != 0:
#        continue
#    if cluster >= 1 and cluster < df_d.shape[0]:
#        job = pool.apply_async(silhouette_score, (1 - df_d, labels.values, "precomputed"))
#        jobs.append((cluster, job))
#
#pool.close()
#pool.join()
#
#x = []
#y = []
#for cluster, job in jobs:
#    x.append(cluster)
#    y.append(job.get())
#
#fig = plt.figure()
#plt.plot(x, y)
#plt.xlabel("Cluster")
#plt.ylabel("Silhouette width")
#plt.savefig(outfile2, dpi=300)
#
