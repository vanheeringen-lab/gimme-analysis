# Configuration

The file `config.yaml` contains the configuration:

``` 
gaps:  "data/hg38.gaps.bed"
genome: "/data/genomes/hg38/hg38.fa"
maxpeaks: 100
peak_dir: "data/remap.test"
pfm_dir: "data/pfm.test"
reference: "gimme.vertebrate.v5.0"
```

You will need to have the hg38 genome FASTA file available (shameless plug: use [genomepy](https://github.com/simonvh/genomepy)).
The `peak_dir` is set to `data/remap.test` and the `pfm_dir` to `data/pfm.test`. These are small data sets to check this to see if the workflow works. The variable `maxpeaks` selects the number of peaks to use (we used 5000 in the manuscript).
Use the script `scripts/download_remap_peaks.sh` to download all the remap peaks to the directory `data/remap`.
By setting `pfm_dir` to `data/pfm` all motif files named `*.pfm` in that directory will be included for comparison. 
The `reference` determines which motif database will be used as a reference for figure1a.png.

When the workflow is finished, the directory `out/` will contain several
`final.*.txt` files that contain all the metrics.

# Run

Install snakemake and gimmemotifs using conda:

``` 
conda create -n db_comparison python=3 snakemake gimmemotifs
```

Activate the environment:

```
conda activate db_comparison
```

Dry run: 

```
snakemake -n
```

Full run:
``` 
snakemake --use-conda -j 12 --resources mem_mb=12000
``` 

Change the `-j 12` to your preferred number of cores and `--resources
mem_mb=12000` to change the available memory (in MBs).
See `cluster.json` and the script `submit_snakemake.sh` for an example on how to
run the workflow on a cluster (SLURM in this case).
