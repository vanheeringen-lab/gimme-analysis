# Three examples of using GimmeMotifs

This repository contains the analysis code of the manuscript describing the 2018 release of GimmeMotifs, an analysis framework for transcription factor motif analysis. The manuscript is available on [biorRxiv](https://doi.org/10.1101/474403) as a preprint and can be cited as:

> [**GimmeMotifs: an analysis framework for transcription factor motif analysis**](https://doi.org/10.1101/474403) <br>
Niklas Bruse, Simon J. van Heeringen<br>
_bioRxiv_ (2018) DOI: [10.1101/474403](https://doi.org/10.1101/474403)

The manuscript source can be found at [https://github.com/simonvh/gimmemotifs-manuscript](https://github.com/simonvh/gimmemotifs-manuscript).

## Motif database benchmark

We evaluated nine different TF motif databases using ChIP-seq peaks from [ReMap](http://pedagogix-tagc.univ-mrs.fr/remap/). 

For the workflow, see the [motif_database_comparison](motif_database_comparison).

## Benchmark of de novo motif finders

For the workflow see [de_novo_benchmark](de_novo_benchmark).

## Motif activity in hematopoietic enhancers

The analysis is detailed in [this
notebook](https://github.com/vanheeringen-lab/gimme-analysis/blob/master/hematopoietic_enhancers/maelstrom_hematopoietic_H3K27ac.ipynb).

## GimmeMotifs vertebrate v5.0

The pipeline that was used to create the clustered, non-redundant motif database GimmeMotifs vertebrate v5.0 can be found here: [cluster_motifs](cluster_motifs).
