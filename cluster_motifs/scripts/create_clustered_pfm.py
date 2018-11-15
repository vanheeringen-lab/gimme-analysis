from collections import Counter
import glob
import os
import re
import sys

import numpy as np
import pandas as pd

from gimmemotifs.motif import read_motifs
from gimmemotifs.comparison import MotifComparer
from gimmemotifs.config import MotifConfig

def get_clustered_motifs(motif_ids):
    ave = motifs[motif_ids[0]]
    for m in motif_ids[1:]:
        if m in motifs:
            score, pos, strand = mc.compare_motifs(m1=ave, m2=motifs[m], match="total", metric="wic")
            ave = ave.average_motifs(motifs[m], pos, strand)
    ave.trim()
    return ave

def factors2label(factors, anno, col="Family_Name"):
    label = ""
    if anno.index.isin(factors).sum() > 0:
        unique_fam =  sorted(list(set(anno.loc[factors, "Family_Name"].dropna().values)))
        if len(unique_fam) > 1:
            cnt = Counter(anno.loc[factors, "Family_Name"].dropna().values) 
            s_keys = sorted(cnt.keys(), key=lambda x: cnt[x])
            if cnt[s_keys[-1]] > cnt[s_keys[-2]]:
                label = s_keys[-1]
            else:
                label = "Mixed"
        else:
            label = unique_fam[0]
    else:
        label = "Unknown"
    label = re.sub("[ /,]+", "_", label)
    return label


pfmfile = "data/20181017.all.pfm"
clusterfile = "out/cluster_table.seqcor.ed0.conn1.txt.gz"
version = "5.0"
outname = "out/gimme.vertebrate.v{}".format(version)
k = 1900
tf_info = "/data/cis-bp-1.02/TF_Information_all_motifs.txt"

# Get motif dir from the GimmeMotifs installation
m2f_dir = MotifConfig().get_motif_dir()
m2f = {}
fnames = glob.glob(os.path.join(m2f_dir,"*.motif2factors.txt"))
for fname in fnames:
    with open(fname) as f:
        for line in f:
            vals = line.strip().split("\t")
            if len(vals) == 4:
                m2f[vals[0]] = m2f.get(vals[0], []) + [vals[1:]]
#print(m2f)

# Read factor to family mapping from the CIS-BP databse
anno = pd.read_table(tf_info)
anno = anno[["TF_Name", "Family_Name"]].drop_duplicates().set_index("TF_Name")

# read motifs
motifs = dict([(m.id, m) for m in read_motifs(open(pfmfile))])
df_cluster = pd.read_table(clusterfile)

ic_cutoff = 5
mc = MotifComparer()
id_count = {}
df = df_cluster.loc[k]
sys.stderr.write(str(k) + "\n")
seen_line = {}
with open("{}.pfm".format(outname), "w") as out:
    with open("{}.motif2factors.txt".format(outname), "w") as m2f_out:
        print("Motif\tFactor\tEvidence\tCurated", file=m2f_out)
        for cluster in range(k):
            if cluster % 10 == 0:
                sys.stderr.write("{}\n".format(cluster))
                out.flush()
            motif_ids = df[df == cluster].index
            motif = get_clustered_motifs(motif_ids)
            if motif.information_content() >= ic_cutoff:
                factors = []
                for m_id in motif_ids:
                    factors += [row[0] for row in m2f.get(m_id, [])]
                label = factors2label(factors, anno)
                id_count[label] = id_count.get(label, 0) + 1
                motif.id = "GM.{}.{}.{:04d}".format(version, label, id_count[label])
                out.write("#{}\t{}\n".format(motif.id, ";;".join(motif_ids)))
                out.write("{}\n".format(motif.to_pwm()))

                for m_id in motif_ids:
                    if m_id in m2f:
                        for row in m2f[m_id]:
                            line = "{}\t{}\t{}\t{}\n".format(motif.id, *row)
                            if line not in seen_line:
                                m2f_out.write(line)
                                seen_line[line] = 1
