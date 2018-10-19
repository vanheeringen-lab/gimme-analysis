Configuration
=============

The file `config.yaml` contains the configuration:

``` 
gaps:  "data/hg38.gaps.bed"
genome: "/data/genomes/hg38/hg38.fa"
maxpeaks: 5000
peak_dir: "test_peaks"
reference: "gimme.vertebrate.v3.1"
```

Please update this where necessary. 
For the ENCODE peaks you will need to have hg19 installed (shameless plug: use [genomepy](https://github.com/simonvh/genomepy)).
The `peak_dir` is set to `test_peaks` by default. 
You can check this to see if the workflow works. 
The directory `peaks` contains all peaks, but this workflow will take a while!
The `reference` determines which motif database will be used as a reference for figure3b.png.

Install snakemake using conda:

``` 
conda install snakemake
```

Dry run! 

```
snakemake -n
```

Full run.
``` 
snakemake --use-conde
``` 
