import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import glob
import numpy as np
import sys

sns.set_style('white')

tools = sys.argv[1].strip().split(",")

df = pd.DataFrame(index=tools)
total_df = pd.DataFrame()
for fname in glob.glob("out/*txt"):
    tmp = pd.read_table(fname)
    tmp["tool"] = tmp["tool"].str.replace("^m\d+$", "GADEM")
    tmp = df.join(tmp.groupby("tool").max())
    
    idx = np.any(tmp.isnull(), 1)
    tmp["source"] = tmp[~idx]["source"][0]
    tmp.loc[idx, "roc_auc"] = 0.5
    tmp.loc[idx, "mncp"] = 1.0
    tmp.loc[idx, "recall_at_fdr"] = 0.0
    tmp["rank"] = tmp.rank()[["roc_auc", "mncp", "recall_at_fdr"]].mean(axis=1)
    
    total_df = pd.concat((total_df, df.join(tmp).reset_index()))
total_df.columns = ["tool"] + list(total_df.columns[1:])
total_df['index'] = range(total_df.shape[0])
total_df = total_df.set_index("index")

fname = total_df["source"].str.split("/", expand=True).iloc[:,-1]
factor = fname.str.replace("^.*(Tfbs|Chip|Histone)[A-Z][a-z0-9]*([A-Z][a-z0-9]+).*_.*$", "\\2")
total_df["factor"] = factor.str.replace("(sc|ab)\d+$", "")

median_df = total_df.groupby(["tool", "factor"]).median().reset_index()

bins = pd.DataFrame(pd.cut(median_df.groupby("factor").median()["roc_auc"], 5))
bins.columns = ["bin"]
median_df = median_df.join(bins, on="factor")


# Figure 4a
ensemble = total_df.groupby("source").max().groupby("factor").median().reset_index()
ensemble["tool"] = "best"
tmp = pd.concat((median_df, ensemble))
order = tmp.groupby("tool").median()["roc_auc"].sort_values().index
sns.factorplot(y="tool", x="roc_auc", data=tmp,
              kind="box", size=6, order=order)
plt.savefig("out/figure4a.svg")

# Figure 4b
pal = sns.color_palette()
metric = "recall_at_fdr"
flop = median_df.join(median_df.groupby("factor").max()[metric], on="factor", rsuffix="_max")
flop["{}_diff".format(metric)] = flop[metric] - flop["{}_max".format(metric)] 
flop = flop[flop["factor"].isin(flop[flop["recall_at_fdr"] > 0]["factor"].unique())]
order = list(flop.groupby("tool").median().sort_values("{}_diff".format(metric)).index)
fp = sns.factorplot(y="tool", x="{}_diff".format(metric), data=flop,
              kind="box", size=4, order=order, color=pal[0])
plt.xlim(-0.45, 0)
plt.xlabel("Difference compared to best motif")
plt.title("Recall at 10% FDR")
sns.despine(left=True)
plt.savefig("out/figure4b.svg")

# Figure 4c
cg = sns.clustermap(median_df.groupby(["tool", "bin"]).mean()["rank"].reset_index().set_index("tool").pivot(columns="bin").fillna(0),
               col_cluster=False,figsize=(2,4), cmap="viridis", metric="correlation", xticklabels=False)
plt.setp(cg.ax_heatmap.yaxis.get_majorticklabels(), rotation=0);
plt.title("Rank as function of motif strength")
plt.savefig("out/figure4c.svg")


