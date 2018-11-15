Configuration
=============

The file `config.yaml` contains the configuration:

``` 
# Reference genome
genome: "/data/genomes/hg19/hg19.fa"
# Top peaks to use for de novo motif search
maxpeaks: 5000
# size of region to look for motifs
size: 100
# File containing http links to bb peak files
peak_file: "data/test_peaks.txt"
# Which de novo motif prediction tools to compare
#tools: MDmodule,Homer,BioProspector,MEME,MEMEW,GADEM,MotifSampler,trawler,Improbizer,Posmo,ChIPMunk,AMD,HMS,XXmotif,Weeder
tools: MDmodule,Homer,BioProspector,ChIPMunk
```

Please update this where necessary. 
For the ENCODE peaks you will need to have hg19 installed (shameless plug: use [genomepy](https://github.com/simonvh/genomepy)).

Install the workflow dependencies using conda:

```
conda env create -n de_novo_benchmark --file environment.yaml
```

Activate the enviroment.

``` 
source activate de_novo_benchmark
```

And (dry)run! Remove the `-n` to really run.

```
snakemake --use-conda -n
```
