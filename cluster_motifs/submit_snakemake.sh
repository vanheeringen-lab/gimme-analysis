#!/bin/bash
#SBATCH -N 1
#SBATCH -t 10:00:00

source activate cluster_workflow
snakemake -j 500 --use-conda --cluster-config cluster.json --cluster "sbatch -N {cluster.N} -t {cluster.time} -p {cluster.partition}"

