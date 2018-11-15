# Reproduce the final steps

You can download intermediate files at Zenodo: DOI LINK. Put both of these files in the `out/` directory. 
Download the CIS-BP TF information: http://cisbp.ccbr.utoronto.ca/data/1.02/DataFiles/Bulk_downloads/EntireDataset/TF_Information_all_motifs.txt.zip. Unzip the file.
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

