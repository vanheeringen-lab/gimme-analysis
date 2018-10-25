import pandas as pd

fnames = snakemake.input
outfile = snakemake.output[0]
dfs = [pd.read_table(fname, index_col=0) for fname in fnames]
df = pd.concat(dfs)
compression = None
if outfile.endswith(".gz"):
    compression = "gzip"
df.to_csv(outfile, sep="\t", compression=compression)
