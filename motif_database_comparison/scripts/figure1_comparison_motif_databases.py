import os
import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

font = 'Nimbus Sans L'  # an open type font
plt.rcParams["font.family"] = font
plt.rcParams['font.size'] = 12
plt.rcParams['svg.fonttype'] = 'none'

reference = sys.argv[1]
outdir = sys.argv[2]

df_auc = pd.read_table(
        os.path.join(outdir, "final.ROC_AUC.table.txt"), 
        index_col=0)
df_recall = pd.read_table(
        os.path.join(outdir, "final.Recall_10FDR.table.txt"), 
        index_col=0)

order = {
        "factorbook": 1,
        "HOMER": 2,
        "HOCOMOCOv11_HUMAN": 3,
        "SwissRegulon": 4,
        "JASPAR2018_vertebrates": 5,
        "IMAGE": 6,
        "ENCODE": 7,
        "RSAT_vertebrates": 8,
        }
colmap = {
    'JASPAR2018_vertebrates': "JASPAR",
    'RSAT_vertebrates': 'RSAT',
    'HOCOMOCOv11_HUMAN': 'HOCOMOCO',
}


ignore = []

sns.set_style('white') 
size = 3
df_plot = df_recall 
pal = sns.color_palette("RdBu", n_colors=7) 
ncols = 3 
cols = [c for c in df_plot.columns if not c in ignore] 
nrows = len(cols) / ncols + 1 
fig = plt.figure(figsize=(5.88,nrows*2))
for i,col in enumerate(sorted([c for c in cols if c != reference], key=lambda x:order.get(x, -1))):
    ax = fig.add_subplot(nrows, ncols, i + 1)
    #plt.plot([0, 1], [0, 1], ls="--", c="grey")
  
    f1 = df_plot[reference] > df_plot[col] + 0.025
    f2 = df_plot[reference] < df_plot[col] - 0.025
    plt.scatter(df_plot[np.logical_and(~f1, ~f2)][col], df_plot[np.logical_and(~f1, ~f2)][reference], c="grey", alpha=0.7, s=size)    
    plt.scatter(df_plot[f2][col], df_plot[f2][reference], c=pal[0], alpha=0.7, s=size)    
    plt.scatter(df_plot[f1][col], df_plot[f1][reference], c=pal[-1], alpha=0.7, s=size)
    plt.xlim(0, 1)
    plt.ylim(0, 1)

    if i < len(cols) - nrows:
        ax.get_xaxis().set_ticklabels([])
    if i % ncols != 0:
        ax.get_yaxis().set_ticklabels([])
    
    ax.text(0.98, 0.02, colmap.get(col, col), 
            horizontalalignment='right',
            verticalalignment='bottom',
           )


plt.savefig(os.path.join(outdir, "figure1b.png"), dpi=300)
plt.savefig(os.path.join(outdir, "figure1b.svg"))
#
#plt.figure()
#cols = [c for c in df_plot.columns if c not in  ["new", "gimme"]]
#pal = sns.color_palette("Set1", len(cols))
#sns.factorplot(y="database", x='ROC AUC', 
#                data=pd.melt(df_auc[cols], value_name="ROC AUC", var_name="database"), 
#                kind="box", palette=pal[1:2],
#                order=df_auc[cols].median(0).sort_values().index)
#
f, ax = plt.subplots(figsize=(5, 5))
sns.set(style="ticks")
df_plot = pd.melt(df_auc[cols], value_name="ROC AUC", var_name="database")
order = df_auc[cols].median(0).sort_values().index
x = "ROC AUC" 
ax = sns.boxplot(data=df_plot, x=x, y="database",palette="Blues" ,
           order=order)
for patch in ax.artists:
    r, g, b, a = patch.get_facecolor()
    patch.set_facecolor((r, g, b, .6))
ax = sns.stripplot(data=df_plot, x=x, y="database", size=3,  color=".3", linewidth=0,
                   jitter=.25, alpha=.5,
                  order=order)
plt.xlim(0.5,1)
ax.xaxis.grid(True)
sns.despine(trim=True, left=True)
plt.tight_layout()
plt.savefig(os.path.join(outdir, "figure1a.png"), dpi=300)
plt.savefig(os.path.join(outdir, "figure1a.svg"))
