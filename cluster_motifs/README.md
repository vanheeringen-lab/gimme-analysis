# Reproduce the final steps

You can download intermediate files at Zenodo ([10.5281/zenodo.1488638](https://doi.org/10.5281/zenodo.1488638)): 

* [cluster_table.seqcor.ed0.conn1.txt.gz](https://zenodo.org/record/1488638/files/cluster_table.seqcor.ed0.conn1.txt.gz?download=1)
* [distance_table.seqcor.txt.gz](https://zenodo.org/record/1488638/files/distance_table.seqcor.txt.gz?download=1)

Put both of these files without gunzipping in the `out/` directory. 
Download the CIS-BP TF information: 

* http://cisbp.ccbr.utoronto.ca/data/1.02/DataFiles/Bulk_downloads/EntireDataset/TF_Information_all_motifs.txt.zip. 

Unzip this file.
Edit the script `scripts/create_clustered_pfm.py` and change the following line to the right location:

```
tf_info = "/data/cis-bp-1.02/TF_Information_all_motifs.txt"
```

By running the script you will re-create the clustered pfm file.

```
python scripts/create_clustered_pfm.py
```

# Run the full pipeline

These steps will reproduce the complete pipeline.

## Configuration

The file `config.yaml` contains the configuration:

``` 
pwm:  "data/20181017.all.pfm"
chunksize: 100
```

## Run

To run this pipeline you will have to install [bioconda](https://bioconda.github.io/).
Install snakemake using conda:

``` 
conda install snakemake
```

Dry run: 

```
snakemake -n
```

Full run using 12 cores:
``` 
snakemake --use-conda --cores 12
``` 

See `cluster.json` and the script `submit_snakemake.sh` for an example on how to
run the workflow on a cluster (SLURM in this case).

