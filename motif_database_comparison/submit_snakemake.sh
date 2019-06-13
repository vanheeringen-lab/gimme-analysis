#!/bin/bash
#SBATCH -N 1
#SBATCH -t 48:00:00

source activate snakemake
snakemake --unlock
snakemake --use-conda -j 500 -k --resources mem_mb=24000 --cluster-config cluster.json --cluster "sbatch -N {cluster.N} -t {cluster.time} -p {cluster.partition}" 
