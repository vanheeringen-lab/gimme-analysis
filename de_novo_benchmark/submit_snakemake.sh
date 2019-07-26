#!/bin/bash
#SBATCH -N 1
#SBATCH -t 02:30:00
#SBATCH -p normal

. $HOME/miniconda3/etc/profile.d/conda.sh
conda activate
conda activate snakemake
snakemake --unlock

snakemake -j 10 --use-conda --cluster-config cluster.json --cluster "sbatch -N 1 -t {cluster.time} -p {cluster.partition}" 
