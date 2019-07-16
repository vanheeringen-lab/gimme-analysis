#!/bin/bash
#SBATCH -N 1
#SBATCH -t 10:00:00

. /home/simonvh/miniconda3/etc/profile.d/conda.sh
conda activate
conda activate snakemake
snakemake -j 500 --use-conda --cluster-config cluster.json --cluster "sbatch -N 1 -t {cluster.time} -p {cluster.partition}" 
