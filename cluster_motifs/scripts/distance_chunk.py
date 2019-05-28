import sys
from gimmemotifs.motif import read_motifs
from gimmemotifs.comparison import seqcor,MotifComparer,_get_all_scores

pwmfile = sys.argv[1]
outfile = sys.argv[2]
chunksize = int(sys.argv[3])
chunk = int(sys.argv[4])
metric = sys.argv[5]

if metric not in ["wic", "seqcor", "pcc", "ed"]:
    raise ValueError("invalid metric {}".format(metric))

all_motifs = read_motifs(open(pwmfile))
chunk_motifs = all_motifs[(chunk -1) * chunksize:chunk * chunksize]

mc = MotifComparer()
if metric == "pcc": 
    dists = mc.get_all_scores(chunk_motifs, all_motifs, "partial", metric, "mean", False)
else: 
    dists = mc.get_all_scores(chunk_motifs, all_motifs, "total", metric, "mean", False)

cols = list(dists.values())[0]
with open(outfile, "w") as f:
    f.write("\t{}\n".format("\t".join(cols)))
    for k,v in dists.items():
        f.write("{}\t{}\n".format(k, "\t".join(["{:.6f}".format(v[c][0]) for c in cols])))

        
