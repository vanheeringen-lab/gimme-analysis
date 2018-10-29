#!/bin/bash
#SBATCH -N 1
#SBATCH -t 10:00:00

source activate snakemake
snakemake --unlock
snakemake --use-conda -j 500 --cluster-config cluster.json --cluster "sbatch -N {cluster.N} -t {cluster.time} -p {cluster.partition}" 
